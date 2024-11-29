import cv2
import tkinter as tk
from tkinter import simpledialog
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import input_cfg

def capture_images_with_gui():
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
    name = simpledialog.askstring("Input", "Enter your name:")
    if not name:
        print("No name entered. Exiting...")
        return  
    print(f"Capturing images for {name}. Press SPACE to capture, 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        cv2.imshow('Frame', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == 32:  
            img_count += 1
            img_filename = f"captured_images/image_{img_count}.jpg"
            cv2.imwrite(img_filename, frame)
            print(f"Captured: {img_filename}")
        elif key == ord('q'):  
            print("Q key pressed. Exiting...")
            break
    cap.release()
    cv2.destroyAllWindows()
    root.quit()

if __name__ == "__main__":
    capture_images_with_gui()
