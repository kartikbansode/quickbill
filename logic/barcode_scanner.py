import cv2
from pyzbar import pyzbar
import threading
import time
from logic.config import get
from logic.resource_path import resource_path
import pygame

# ============================================================
# SOUND
# ============================================================

SCAN_SOUND = None

try:
    pygame.mixer.init(
        frequency=44100,
        size=-16,
        channels=2,
        buffer=256,
    )

    SCAN_SOUND = pygame.mixer.Sound(resource_path("assets/sounds/beep.mp3"))

    SCAN_SOUND.set_volume(0.8)

except Exception as e:
    print(f"[WARNING] Sound disabled: {e}")


# ============================================================
# SCANNER SETTINGS
# ============================================================

# Prevent the same barcode from being repeatedly detected
# while it remains in front of the camera.
# SCAN_COOLDOWN = 0.25

# Maximum processing width.
# Keeping this around 1280 gives good barcode accuracy
# without unnecessarily increasing CPU usage.
MAX_PROCESS_WIDTH = 1280

# Decode rotated frames only when needed.
# The normal frame is always tried first.
ENABLE_ROTATION_SCAN = True

# Scan full frame.
# This is important because the old narrow ROI could cut
# off barcodes depending on their position/orientation.
USE_FULL_FRAME = True


# ============================================================
# GLOBAL STATE
# ============================================================

stop_scanning = False
scanner_thread = None

visible_codes = set()

# Last time each barcode was successfully detected.
# This prevents temporary frame drops from being interpreted
# as the barcode leaving the camera.
last_seen_time = {}

# Barcode must remain undetected for this long before it
# becomes eligible for another scan.
BARCODE_ABSENCE_TIMEOUT = 1.2


# ============================================================
# SOUND
# ============================================================


def play_beep():

    if SCAN_SOUND is None:
        return

    try:

        SCAN_SOUND.stop()
        SCAN_SOUND.play()

    except Exception:
        pass


# ============================================================
# IMAGE PREPARATION
# ============================================================


def resize_for_processing(image):
    """
    Limit processing resolution while preserving aspect ratio.
    """

    if image is None:
        return None

    height, width = image.shape[:2]

    if width <= MAX_PROCESS_WIDTH:
        return image

    scale = MAX_PROCESS_WIDTH / float(width)

    new_width = int(width * scale)
    new_height = int(height * scale)

    return cv2.resize(
        image,
        (new_width, new_height),
        interpolation=cv2.INTER_AREA,
    )


def prepare_frames(gray):
    """
    Generate several views of the same camera frame.

    The first frame is the normal orientation.

    Additional frames are rotated 90 degrees in both
    directions so barcodes can be detected regardless
    of their physical orientation.
    """

    frames = []

    if gray is None:
        return frames

    # --------------------------------------------------------
    # 1. Original orientation
    # --------------------------------------------------------

    frames.append(gray)

    # --------------------------------------------------------
    # 2. Slightly cropped center
    #
    # This helps reduce background noise while still being
    # considerably larger than the old 40% x 50% ROI.
    # --------------------------------------------------------

    h, w = gray.shape

    crop = gray[
        int(h * 0.10) : int(h * 0.90),
        int(w * 0.10) : int(w * 0.90),
    ]

    if crop.size > 0:
        frames.append(crop)

    if ENABLE_ROTATION_SCAN:

        # ----------------------------------------------------
        # 3. 90 degree clockwise
        # ----------------------------------------------------

        rotated_clockwise = cv2.rotate(
            gray,
            cv2.ROTATE_90_CLOCKWISE,
        )

        frames.append(rotated_clockwise)

        # ----------------------------------------------------
        # 4. 90 degree counter-clockwise
        # ----------------------------------------------------

        rotated_counter = cv2.rotate(
            gray,
            cv2.ROTATE_90_COUNTERCLOCKWISE,
        )

        frames.append(rotated_counter)

    return frames


def decode_barcode_frames(gray):
    """
    Decode barcodes from multiple orientations.

    Returns a list of unique decoded barcode strings.
    """

    detected = []
    detected_set = set()

    frames = prepare_frames(gray)

    for frame in frames:

        if frame is None:
            continue

        try:

            barcodes = pyzbar.decode(frame)

        except Exception as exc:

            print(f"[SCANNER DECODE ERROR] {exc}")

            continue

        for barcode in barcodes:

            try:

                barcode_data = barcode.data.decode("utf-8").strip()

            except Exception:
                continue

            if not barcode_data:
                continue

            if barcode_data in detected_set:
                continue

            detected_set.add(barcode_data)

            detected.append(barcode_data)

    return detected


# ============================================================
# MAIN SCANNER
# ============================================================

def start_barcode_scanner(
    stream_url,
    on_detected_callback,
):

    global stop_scanning
    global visible_codes
    global last_seen_time

    cap = cv2.VideoCapture(
        stream_url,
        cv2.CAP_FFMPEG,
    )

    # --------------------------------------------------------
    # Camera performance
    # --------------------------------------------------------

    cap.set(
        cv2.CAP_PROP_BUFFERSIZE,
        1,
    )

    cap.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        1280,
    )

    cap.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        720,
    )

    cap.set(
        cv2.CAP_PROP_FPS,
        30,
    )

    if not cap.isOpened():

        print("[X] Could not open video stream.")

        return

    print("=" * 50)
    print("[SCANNER] Started")
    print("[SCANNER] Professional visibility-lock mode")
    print("[SCANNER] Orientation-independent mode")
    print("[SCANNER] Waiting for barcode...")
    print("=" * 50)

    visible_codes.clear()
    last_seen_time.clear()

    while not stop_scanning:

        # ----------------------------------------------------
        # Drop stale network frames.
        # ----------------------------------------------------

        cap.grab()
        cap.grab()

        ret, frame = cap.read()

        if not ret:

            print(
                "[SCANNER] Frame read failed. Reconnecting..."
            )

            cap.release()

            time.sleep(1)

            cap = cv2.VideoCapture(
                stream_url,
                cv2.CAP_FFMPEG,
            )

            cap.set(
                cv2.CAP_PROP_BUFFERSIZE,
                1,
            )

            cap.set(
                cv2.CAP_PROP_FRAME_WIDTH,
                1280,
            )

            cap.set(
                cv2.CAP_PROP_FRAME_HEIGHT,
                720,
            )

            cap.set(
                cv2.CAP_PROP_FPS,
                30,
            )

            continue

        # ----------------------------------------------------
        # Reduce processing resolution if required.
        # ----------------------------------------------------

        frame = resize_for_processing(frame)

        if frame is None:
            continue

        # ----------------------------------------------------
        # Grayscale
        # ----------------------------------------------------

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY,
        )

        # ----------------------------------------------------
        # Decode all supported orientations.
        # ----------------------------------------------------

        decoded_codes = decode_barcode_frames(gray)

        now = time.monotonic()

        current_visible = set()

        # ----------------------------------------------------
        # PROCESS DETECTED BARCODES
        # ----------------------------------------------------

        for barcode_data in decoded_codes:

            if not barcode_data:
                continue

            barcode_data = barcode_data.strip()

            if not barcode_data:
                continue

            current_visible.add(
                barcode_data
            )

            # ------------------------------------------------
            # Update last successful observation.
            #
            # IMPORTANT:
            # Even if the barcode was already scanned,
            # continuously seeing it keeps it locked.
            # ------------------------------------------------

            last_seen_time[
                barcode_data
            ] = now

            # ------------------------------------------------
            # ALREADY SCANNED + STILL PRESENT
            #
            # Never add it again.
            # ------------------------------------------------

            if barcode_data in visible_codes:
                continue

            # ------------------------------------------------
            # NEW BARCODE
            #
            # It has genuinely become visible after previously
            # being absent for the required timeout.
            # ------------------------------------------------

            visible_codes.add(
                barcode_data
            )

            try:

                if get(
                    "scanner",
                    "beep",
                ):
                    play_beep()

            except Exception:
                pass

            try:

                on_detected_callback(
                    barcode_data
                )

            except Exception as e:

                print(
                    "[SCANNER CALLBACK ERROR] "
                    f"{e}"
                )

        # ====================================================
        # DISAPPEARANCE GRACE PERIOD
        # ====================================================
        #
        # DO NOT immediately unlock a barcode just because
        # pyzbar missed it in one frame.
        #
        # A barcode can temporarily disappear because of:
        #
        # - motion blur
        # - camera autofocus
        # - network frame drops
        # - JPEG compression
        # - rotation
        # - poor lighting
        # - temporary occlusion
        #
        # It must remain unseen for BARCODE_ABSENCE_TIMEOUT
        # before it is considered physically removed.
        # ====================================================

        for barcode_data in list(
            visible_codes
        ):

            last_seen = last_seen_time.get(
                barcode_data
            )

            if last_seen is None:

                # Safety fallback.
                last_seen_time[
                    barcode_data
                ] = now

                continue

            absent_for = (
                now - last_seen
            )

            if (
                absent_for
                >= BARCODE_ABSENCE_TIMEOUT
            ):

                # Barcode has genuinely disappeared.
                visible_codes.discard(
                    barcode_data
                )

                last_seen_time.pop(
                    barcode_data,
                    None,
                )

        # ----------------------------------------------------
        # Small sleep prevents unnecessary CPU spinning.
        # ----------------------------------------------------

        time.sleep(0.01)

    cap.release()

    visible_codes.clear()
    last_seen_time.clear()

    print("[SCANNER] Stopped")


# ============================================================
# BACKGROUND SCANNER
# ============================================================

def scan_barcode_background(
    stream_url,
    callback,
):

    global stop_scanning
    global visible_codes
    global last_seen_time
    global scanner_thread

    if (
        scanner_thread is not None
        and scanner_thread.is_alive()
    ):
        return

    stop_scanning = False

    visible_codes.clear()
    last_seen_time.clear()

    scanner_thread = threading.Thread(
        target=start_barcode_scanner,
        args=(
            stream_url,
            callback,
        ),
        daemon=True,
    )

    scanner_thread.start()


# ============================================================
# STOP SCANNER
# ============================================================


def stop_scanner():

    global stop_scanning
    global scanner_thread

    stop_scanning = True

    if scanner_thread and scanner_thread.is_alive():

        scanner_thread.join(timeout=1)

    scanner_thread = None
