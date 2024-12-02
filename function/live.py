import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils import load_yaml
from function.compare import compare

import cv2
import tkinter as tk
from tkinter import simpledialog
import pandas as pd
from os.path import join, exists
from tkinter import messagebox
import argparse
from insightface.app.common import Face

class CameraManager:
    def __init__(self, config: dict):
        self.config = config
        self.faces_dir = config['ObjectDatabase']['dir']
        self.max_faces = self.config['ObjectDatabase']['max_faces']
        self.cap = self._init_camera()
        self.img_count = 0

    def _init_camera(self):
        url = self.config['Camera']['url']
        if not url:
            url = self.config['Camera']['names'][self.config['Camera']['name']]['url']
        cap = cv2.VideoCapture(url)
        if not cap.isOpened():
            print("Error: Could not open video stream")
            return
        return cap

    def _validate_student_code(self, student_code: str):
        sample_data = self.config['SQLDatabase']['sample_data']
        user_sample = join(sample_data, 'users.csv')
        with open(user_sample, 'r') as f:
            users = pd.read_csv(f)
            if student_code not in users['code'].values:
                print(f"Student code {student_code} not found.")
                return False
        return True

    def _get_student_code(self):
        self.root.withdraw()
        student_code = simpledialog.askstring("Input", "Enter your student code:")
        if not student_code:
            print("No student code entered. Exiting...")
            return
        if not self._validate_student_code(student_code=student_code):
            return
        return student_code

    def _is_overwrite(self, student_code: str):
        return messagebox.askyesno("Warning", f"Student code {student_code} already exists. Overwrite?")

    def _prepare_out_dir(self, student_code: str):
        student_code_dir = join(self.faces_dir, student_code)
        if exists(student_code_dir):
            if not self._is_overwrite(student_code):
                available_images = [f for f in os.listdir(student_code_dir) if f.endswith('.jpg')]
                print(f"Available images: {available_images}")
                print(f"Continuing from image count: {len(available_images)}")
                self.img_count = len(available_images)
            else:
                print(f"Overwriting existing images for student code: {student_code}")
                for f in os.listdir(student_code_dir):
                    os.remove(join(student_code_dir, f))

        os.makedirs(student_code_dir, exist_ok=True)
        return student_code_dir

    def capture(self):
        self.root = tk.Tk()
        student_code = self._get_student_code()
        if not student_code:
            return
        student_code_dir = self._prepare_out_dir(student_code)
        
        while True:
            if self.img_count >= self.max_faces:
                print("Max images captured")
                break
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            cv2.imshow('Frame', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == 32:  
                self.img_count += 1
                img_filename = join(student_code_dir, f"{self.img_count}.jpg")
                cv2.imwrite(img_filename, frame)
                print(f"Captured: {img_filename}")
            elif key == ord('q'):  
                print("Q key pressed. Exiting...")
                break

        self.cap.release()
        cv2.destroyAllWindows()
        self.root.quit()

    def live(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            results = compare(frame, self.config)
            if not results:
                cv2.imshow('Frame', frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("Q key pressed. Exiting...")
                    break
                continue
            student_code, certainty, bbox = results
            student_code = student_code if student_code else "Unknown"
            x1, y1, x2, y2 = map(int, bbox[:4])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{student_code} ({certainty:.2f})", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            cv2.imshow('Frame', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("Q key pressed. Exiting...")
                break

        self.cap.release()
        cv2.destroyAllWindows()

def parse_args():
    parser = argparse.ArgumentParser(description="Capture images from camera")
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to config file')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    config = load_yaml(args.config)
    camera_manager = CameraManager(config)
    camera_manager.live()