
import cv2
import math
import time
import numpy as np
import sys

import handtrackingmodule as htm


# Pycaw is Windows-specific.
if sys.platform != "win32":
    raise OSError(
        "Volume control currently supports Windows only."
    )

from pycaw.pycaw import AudioUtilities


# ==========================================
# CAMERA CONFIGURATION
# ==========================================

W_CAM = 640
H_CAM = 480

CAMERA_INDEX = 0

WINDOW_NAME = "AI Hand Gesture Volume Controller"


# ==========================================
# HAND DISTANCE CONFIGURATION
# ==========================================

MIN_HAND_DISTANCE = 35
MAX_HAND_DISTANCE = 200

# Mute/unmute thresholds.
MUTE_DISTANCE = 35
UNMUTE_DISTANCE = 45

# Volume smoothing.
SMOOTHING_FACTOR = 0.25


# ==========================================
# VOLUME BAR CONFIGURATION
# ==========================================

BAR_MIN = 150
BAR_MAX = 400

BAR_X1 = 50
BAR_X2 = 85


# ==========================================
# MAIN APPLICATION
# ==========================================

def main():

    cap = None
    detector = None

    try:

        # ======================================
        # CAMERA INITIALIZATION
        # ======================================

        cap = cv2.VideoCapture(CAMERA_INDEX)

        cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            W_CAM
        )

        cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            H_CAM
        )

        if not cap.isOpened():

            raise RuntimeError(
                "Unable to access webcam. "
                "Check camera connection and permissions."
            )

        # ======================================
        # HAND DETECTOR INITIALIZATION
        # ======================================

        detector = htm.HandDetector(
            maxHands=1,
            detectionCon=0.7,
            trackCon=0.7
        )

        # ======================================
        # SYSTEM VOLUME INITIALIZATION
        # ======================================

        # Get default audio output device.
        devices = AudioUtilities.GetSpeakers()

        # Access endpoint volume.
        volume = devices.EndpointVolume

        # Read current system volume.
        currentVol = volume.GetMasterVolumeLevelScalar()

        # Initialize smoothing.
        smoothedVol = currentVol

        # Read current mute state.
        is_muted = volume.GetMute()

        # ======================================
        # FPS INITIALIZATION
        # ======================================

        pTime = 0

        # ======================================
        # MAIN APPLICATION LOOP
        # ======================================

        while True:

            success, img = cap.read()

            if not success or img is None:

                print("Unable to read webcam frame.")
                break

            # Mirror webcam image.
            img = cv2.flip(img, 1)

            # ==================================
            # HAND DETECTION
            # ==================================

            img = detector.findHands(
                img,
                draw=True
            )

            lmList = detector.findPosition(
                img,
                handNo=0,
                draw=False
            )

            # ==================================
            # VOLUME CONTROL
            # ==================================

            if len(lmList) == 21:

                # Thumb tip coordinates.
                x1, y1 = (
                    lmList[4][1],
                    lmList[4][2]
                )

                # Index finger tip coordinates.
                x2, y2 = (
                    lmList[8][1],
                    lmList[8][2]
                )

                # Calculate midpoint.
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2

                # Calculate Euclidean distance.
                length = math.hypot(
                    x2 - x1,
                    y2 - y1
                )

                # ==================================
                # DRAW HAND INDICATORS
                # ==================================

                cv2.circle(
                    img,
                    (x1, y1),
                    12,
                    (255, 0, 255),
                    cv2.FILLED
                )

                cv2.circle(
                    img,
                    (x2, y2),
                    12,
                    (255, 0, 255),
                    cv2.FILLED
                )

                cv2.circle(
                    img,
                    (cx, cy),
                    10,
                    (255, 0, 255),
                    cv2.FILLED
                )

                cv2.line(
                    img,
                    (x1, y1),
                    (x2, y2),
                    (255, 0, 255),
                    3
                )

                # ==================================
                # MUTE / UNMUTE CONTROL
                # ==================================

                if length <= MUTE_DISTANCE:

                    if not is_muted:

                        volume.SetMute(True, None)
                        is_muted = True

                    smoothedVol = 0.0

                elif length >= UNMUTE_DISTANCE:

                    if is_muted:

                        volume.SetMute(False, None)
                        is_muted = False

                    # Map distance to volume percentage.
                    volPer = int(
                        np.interp(
                            length,
                            [
                                UNMUTE_DISTANCE,
                                MAX_HAND_DISTANCE
                            ],
                            [0, 100]
                        )
                    )

                    volPer = max(
                        0,
                        min(100, volPer)
                    )

                    # Convert percentage to scalar volume.
                    targetVol = volPer / 100.0

                    # Apply exponential smoothing.
                    smoothedVol = (
                        SMOOTHING_FACTOR * targetVol
                        + (1 - SMOOTHING_FACTOR) * smoothedVol
                    )

                    # Update Windows system volume.
                    volume.SetMasterVolumeLevelScalar(
                        float(smoothedVol),
                        None
                    )

                # ==================================
                # VOLUME DISPLAY VALUES
                # ==================================

                if is_muted:

                    volPer = 0
                    volBar = BAR_MAX

                else:

                    # Read actual system volume.
                    actualVol = (
                        volume.GetMasterVolumeLevelScalar()
                    )

                    volPer = int(actualVol * 100)

                    volBar = int(
                        np.interp(
                            actualVol,
                            [0, 1],
                            [BAR_MAX, BAR_MIN]
                        )
                    )

                # ==================================
                # DRAW VOLUME BAR
                # ==================================

                cv2.rectangle(
                    img,
                    (BAR_X1, BAR_MIN),
                    (BAR_X2, BAR_MAX),
                    (255, 0, 0),
                    3
                )

                cv2.rectangle(
                    img,
                    (BAR_X1, volBar),
                    (BAR_X2, BAR_MAX),
                    (255, 0, 0),
                    cv2.FILLED
                )

                # Display volume percentage.
                cv2.putText(
                    img,
                    f"Volume: {volPer}%",
                    (120, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 0, 0),
                    2
                )

                # Display finger distance.
                cv2.putText(
                    img,
                    f"Distance: {int(length)}",
                    (120, 115),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

                # Display mute status.
                status = "MUTED" if is_muted else "ACTIVE"

                status_color = (
                    (0, 0, 255)
                    if is_muted
                    else (0, 255, 0)
                )

                cv2.putText(
                    img,
                    f"Audio: {status}",
                    (120, 150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    status_color,
                    2
                )

                # Change midpoint color when muted.
                if is_muted:

                    cv2.circle(
                        img,
                        (cx, cy),
                        12,
                        (0, 0, 255),
                        cv2.FILLED
                    )

            else:

                # No hand detected.
                cv2.putText(
                    img,
                    "Show your hand to control volume",
                    (100, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )

            # ==================================
            # FPS CALCULATION
            # ==================================

            cTime = time.time()

            fps = (
                0 if pTime == 0
                else 1 / (cTime - pTime)
            )

            pTime = cTime

            cv2.putText(
                img,
                f"FPS: {int(fps)}",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2
            )

            # ==================================
            # DISPLAY APPLICATION WINDOW
            # ==================================

            cv2.imshow(
                WINDOW_NAME,
                img
            )

            # Process keyboard events.
            key = cv2.waitKey(1) & 0xFF

            # Exit using Q.
            if key == ord("q"):
                break

            # Exit using window close button.
            try:

                if cv2.getWindowProperty(
                    WINDOW_NAME,
                    cv2.WND_PROP_VISIBLE
                ) < 1:
                    break

            except cv2.error:
                break

    finally:

        # ======================================
        # RESOURCE CLEANUP
        # ======================================

        if cap is not None:
            cap.release()

        if detector is not None:
            detector.close()

        cv2.destroyAllWindows()

        print("Volume Hand Controller closed successfully.")


# ==========================================
# DIRECT EXECUTION SUPPORT
# ==========================================

if __name__ == "__main__":
    main()
