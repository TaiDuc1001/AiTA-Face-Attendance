import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils import load_yaml

import cv2
import tkinter as tk
from tkinter import simpledialog
import pandas as pd
from os.path import join, exists
from tkinter import messagebox
import argparse

def validate_student_code(
    student_code: str,
    sample_data: str
):
    if not student_code:
        print("Student code cannot be empty.")
        return False
    user_sample = join(sample_data, 'users.csv')
    with open(user_sample, 'r') as f:
        users = pd.read_csv(f)
        if student_code not in users['code'].values:
            print(f"Student code {student_code} not found.")
            return False

def is_exists(
    student_code: str,
    faces_dir: str
):
    faces_dir = join(faces_dir, student_code)
    if exists(faces_dir):
        print(f"Student code {student_code} already exists.")
        return True
    return False

def capture_images_with_gui(config_path):
    config = load_yaml(config_path)
    input_cfg = config['Camera']
    faces_dir = config['ObjectDatabase']['dir']
    sample_data = config['SQLDatabase']['sample_data']

    url = input_cfg.names[input_cfg.name]['url']
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        print("Error: Could not open video stream")
        return
    
    if not os.path.exists('captured_images'):
        os.makedirs('captured_images')
    img_count = 0
    root = tk.Tk()
    root.withdraw()  
    student_code = simpledialog.askstring("Input", "Enter your student code:")
    if not student_code:
        print("No student code entered. Exiting...")
        return
    if not validate_student_code(student_code=student_code, sample_data=sample_data):
        return
    
    student_code_dir = join(faces_dir, student_code)

    if is_exists(student_code=student_code, faces_dir=faces_dir):
        overwrite = messagebox.askyesno("Overwrite Confirmation", "Do you want to overwrite the existing images?")
        if overwrite != 'y':
            continue_capture = messagebox.askyesno("Continue Confirmation", "Do you want to continue capturing images?")
            if not continue_capture:
                return
        else:
            os.system(f'rm -rf {student_code_dir}')
    
    if continue_capture:
        os.makedirs(student_code_dir)
        img_count = len(os.listdir(student_code_dir))

    max_images = 3
    print(f"Capturing images for {student_code}. Press SPACE to capture, 'q' to quit.")
    while True:
        if img_count >= max_images:
            print("Max images captured")
            break
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow('Frame', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 32:  
            img_count += 1
            img_filename = join(student_code_dir, f"{student_code}_{img_count}.jpg")
            cv2.imwrite(img_filename, frame)
            print(f"Captured: {img_filename}")
        elif key == ord('q'):  
            print("Q key pressed. Exiting...")
            break

    cap.release()
    cv2.destroyAllWindows()
    root.quit()

def parse_args():
    parser = argparse.ArgumentParser(description="Capture images for face recognition")
    parser.add_argument("--config", type=str, help="Path to configuration file", default="config.yaml")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    capture_images_with_gui(config_path=args.config)