import cv2
from pyzbar import pyzbar
import threading
import time
import winsound

stop_scanning = False
last_scanned = ""
last_time = 0
scanner_thread = None


def play_beep():
    try:
        winsound.MessageBeep(winsound.MB_OK)
    except:
        pass


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
            if (
                barcode_data != last_scanned or (now - last_time) > 1
            ):  # ⏱ Delay for same scan
                last_scanned = barcode_data
                last_time = now
                on_detected_callback(barcode_data)

        time.sleep(0.01)

    cap.release()
    print("[!] Scanner stopped.")


def scan_barcode_background(stream_url, callback):

    global stop_scanning
    global scanner_thread

    if scanner_thread is not None and scanner_thread.is_alive():
        return

    stop_scanning = False

    scanner_thread = threading.Thread(
        target=start_barcode_scanner,
        args=(stream_url, callback),
        daemon=True,
    )

    scanner_thread.start()


def stop_scanner():

    global stop_scanning
    global scanner_thread

    stop_scanning = True

    scanner_thread = None