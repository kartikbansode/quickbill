import cv2
from pyzbar import pyzbar
import threading
import time
import playsound

stop_scanning = False
last_scanned = ""
last_time = 0

def play_beep():
    try:
        playsound.playsound("assets/sounds/beep.mp3", block=False)
    except:
        print("[WARN] Beep sound failed")

def start_barcode_scanner(stream_url, on_detected_callback):
    global stop_scanning, last_scanned, last_time
    cap = cv2.VideoCapture(stream_url)

    if not cap.isOpened():
        print("[X] Could not open video stream.")
        return

    print("[OK] Scanner started.")
    while not stop_scanning:
        ret, frame = cap.read()
        if not ret:
            continue

        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")

            now = time.time()
            if barcode_data != last_scanned or (now - last_time) > 1:  # ⏱ Delay for same scan
                last_scanned = barcode_data
                last_time = now
                on_detected_callback(barcode_data)

        cv2.waitKey(1)

    cap.release()
    print("[!] Scanner stopped.")

def scan_barcode_background(stream_url, callback):
    global stop_scanning
    stop_scanning = False
    threading.Thread(target=start_barcode_scanner, args=(stream_url, callback), daemon=True).start()

def stop_scanner():
    global stop_scanning
    stop_scanning = True
