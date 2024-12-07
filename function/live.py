import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils import load_yaml
from function.compare import compare
from function.make_model import get_model

import cv2
import pandas as pd
from os.path import join, exists
import argparse
from queue import Queue
import threading
import onnxruntime as ort
import time
import tkinter as tk
from tkinter import simpledialog, messagebox

ort.set_default_logger_severity(3)

class CameraManager:
    def __init__(self, config: dict):
        self.config = config
        self.faces_dir = config['ObjectDatabase']['names'][config['ObjectDatabase']['name']]
        self.max_faces = self.config['ObjectDatabase']['max_faces']
        self.img_count = 0
        self.skip_frames = 10
        self.detector = get_model(type='Detector', models_cfg=config)
        self.recognizer = get_model(type='Recognizer', models_cfg=config)
        self.frame_queue = Queue(maxsize=5)
        self.result_queue = Queue(maxsize=5)
        self.running = False
        
        self.cap = self._init_camera()
        if self.cap is None:
            sys.exit(1)
            
        self.running = True

    def _init_camera(self):
        url = self.config['Camera']['url']
        if not url:
            url = self.config['Camera']['names'][self.config['Camera']['name']]['url']
        print(f"Attempting to open camera at: {url}")
        cap = cv2.VideoCapture(url)
        if not cap.isOpened():
            return None
        
        ret, frame = cap.read()
        if not ret or frame is None:
            return None
            
        print("Camera initialized successfully")
        return cap

    def _frame_producer(self):
        print("Frame producer started")
        frame_count = 0
        while self.running:
            try:
                if not self.cap.isOpened():
                    print("Camera is not open")
                    break

                ret, frame = self.cap.read()
                if not ret or frame is None:
                    if not self.running:
                        break
                    print("Failed to grab frame")
                    time.sleep(0.1)  
                    continue

                frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                frame_count += 1
                if frame_count % 30 == 0:  
                    print(f"Processed {frame_count} frames")

                if not self.frame_queue.full():
                    self.frame_queue.put(frame)
                else:
                    
                    time.sleep(0.01)
            except cv2.error as e:
                print(f"OpenCV error: {e}")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                break

    def _frame_consumer(self):
        print("Frame consumer started")
        while self.running:
            if self.frame_queue.empty():
                time.sleep(0.01)  
                continue
                
            frame = self.frame_queue.get()
            try:
                results = compare(
                    frame=frame,
                    config=self.config,
                    detector=self.detector,
                    recognizer=self.recognizer
                )
                if results:
                    self.result_queue.put((frame, results))
                else:
                    
                    self.result_queue.put((frame, (None, 0, [0,0,0,0])))
            except Exception as e:
                print(f"Error in frame consumer: {e}")
                continue

    def live(self):
        if not self.running:
            return
        
        producer_thread = threading.Thread(target=self._frame_producer, daemon=True)
        consumer_thread = threading.Thread(target=self._frame_consumer, daemon=True)

        producer_thread.start()
        consumer_thread.start()

        # Create OpenCV window
        cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
        
        print("Starting main loop")
        last_frame_time = time.time()

        while self.running:
            current_time = time.time()
            if current_time - last_frame_time > 5:  
                print("No frames received for 5 seconds")
                last_frame_time = current_time

            if not self.result_queue.empty():
                frame, results = self.result_queue.get()
                last_frame_time = time.time()
                student_code, certainty, bbox = results
                if results[-1] is not None:
                    x1, y1, x2, y2 = map(int, results[-1])
                    cv2.rectangle(frame, (x1, y1), (2*x2 - x1, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{student_code} ({certainty:.2f})", (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
                cv2.imshow("Frame", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("Q key pressed. Exiting...")
                self.running = False
                break

        print("Cleaning up...")
        self.cap.release()
        cv2.destroyAllWindows()

    def capture(self):
        root = tk.Tk()
        root.withdraw()
        while True:
            student_code = simpledialog.askstring("Input", "Enter student code:")
            
            if not student_code:
                messagebox.showerror("Error", "Student code cannot be empty")
                if not messagebox.askretrycancel("Retry", "Do you want to try again?"):
                    root.destroy()
                    return
                continue
            
            user_data = pd.read_csv(join(self.config['SQLDatabase']['sample_data'], 'users.csv'))
            if student_code not in user_data['code'].values:
                messagebox.showerror("Error", "Student code does not exist")
                if not messagebox.askretrycancel("Retry", "Do you want to try again?"):
                    root.destroy()
                    return
                continue
            
            break
        
        student_dir = join(self.faces_dir, student_code)
        if exists(student_dir):
            if messagebox.askyesno("Overwrite", "Student already has images. Overwrite?"):
                for file in os.listdir(student_dir):
                    os.remove(join(student_dir, file))
            else:
                return
        else:
            os.makedirs(student_dir)
        
        root.destroy()
        
        self.running = True
        cv2.namedWindow("Capture", cv2.WINDOW_NORMAL)
        print("Press SPACE to capture image, Q to quit")
        
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break
            
            cv2.imshow("Capture", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord(' '):
                img_path = join(student_dir, f"{self.img_count}.jpg")
                cv2.imwrite(img_path, frame)
                print(f"Captured {img_path}")
                self.img_count += 1
                if self.img_count >= self.max_faces:
                    print("Max faces captured")
                    break
            elif key == ord('q'):
                print("Q key pressed. Exiting...")
                break
        
        self.running = False
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
    camera_manager.capture()
    # camera_manager.live()
