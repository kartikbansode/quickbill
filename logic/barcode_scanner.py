import cv2
from pyzbar import pyzbar
import time
import os
from playsound import playsound
# At top of barcode_scanner.py
scanning = False

def scan_barcode_background(stream_url, timeout=8):
    cap = cv2.VideoCapture(stream_url)

    if not cap.isOpened():
        print("❌ Could not open video stream.")
        return None

    start_time = time.time()
    frame_skip = 2
    count = 0

    while True:
        if time.time() - start_time > timeout:
            break

        ret, frame = cap.read()
        if not ret:
            continue

        count += 1
        if count % frame_skip != 0:
            continue  # skip some frames to save CPU

        # Make it grayscale for faster decoding
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        barcodes = pyzbar.decode(gray)

        if barcodes:
            barcode = barcodes[0].data.decode("utf-8")

            # 🔊 Play beep sound on successful scan
            beep_path = os.path.join("assets", "sounds", "beep.mp3")
            playsound(beep_path)

            cap.release()
            return barcode

    cap.release()
    return None
