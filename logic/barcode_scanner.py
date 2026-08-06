import cv2
from pyzbar import pyzbar
import threading
import time
from logic.config import get
import pygame

pygame.mixer.init(
    frequency=44100,
    size=-16,
    channels=2,
    buffer=256,
)

SCAN_SOUND = pygame.mixer.Sound("assets/sounds/beep.mp3")
SCAN_SOUND.set_volume(0.8)

SCAN_COOLDOWN = 0.25

stop_scanning = False
scanner_thread = None

visible_codes = set()
last_scan_time = {}


def play_beep():
    try:
        SCAN_SOUND.stop()
        SCAN_SOUND.play()
    except Exception as e:
        print(f"Beep error: {e}")


def start_barcode_scanner(stream_url, on_detected_callback):

    global stop_scanning
    global visible_codes
    global last_scan_time
    cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)

    # ---------- Camera Performance ----------

    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)

    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    cap.set(cv2.CAP_PROP_FPS, 30)

    if not cap.isOpened():
        print("[X] Could not open video stream.")
        return

    print("=" * 50)
    print("[SCANNER] Started")
    print("[SCANNER] Waiting for barcode...")
    print("=" * 50)
    visible_codes.clear()
    last_scan_time.clear()
    while not stop_scanning:
        cap.grab()
        cap.grab()
        cap.grab()

        ret, frame = cap.read()
        if not ret:

            cap.release()

            time.sleep(1)

            cap = cv2.VideoCapture(stream_url, cv2.CAP_FFMPEG)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            cap.set(cv2.CAP_PROP_FPS, 30)

            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        h, w = gray.shape

        roi = gray[
            int(h * 0.30) : int(h * 0.70),
            int(w * 0.25) : int(w * 0.75),
        ]

        barcodes = pyzbar.decode(roi)
        if not barcodes:
            visible_codes.clear()
            continue
        current_visible = set()

        for barcode in barcodes:

            barcode_data = barcode.data.decode("utf-8").strip()

            if not barcode_data:
                continue

            current_visible.add(barcode_data)

            # Already visible → ignore
            if barcode_data in visible_codes:
                continue

            now = time.time()

            previous = last_scan_time.get(barcode_data, 0)

            if now - previous < SCAN_COOLDOWN:
                continue

            last_scan_time[barcode_data] = now

            visible_codes.add(barcode_data)

            if get("scanner", "beep"):
                play_beep()

            try:
                on_detected_callback(barcode_data)
            except Exception as e:
                print(f"[SCANNER CALLBACK ERROR] {e}")

        # Remove barcodes that disappeared
        visible_codes.intersection_update(current_visible)

        for code in list(last_scan_time.keys()):

            if code not in visible_codes:

                del last_scan_time[code]

    cap.release()
    print("[SCANNER] Stopped")


def scan_barcode_background(stream_url, callback):

    global stop_scanning
    global visible_codes
    global last_scan_time
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

    if scanner_thread and scanner_thread.is_alive():
        scanner_thread.join(timeout=1)

    scanner_thread = None
