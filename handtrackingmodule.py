import cv2
import mediapipe as mp
import time
from pathlib import Path


class HandDetector:

    # Hand landmark connections.
    HAND_CONNECTIONS = [
        (0, 1), (1, 2), (2, 3), (3, 4),
        (0, 5), (5, 6), (6, 7), (7, 8),
        (5, 9), (9, 10), (10, 11), (11, 12),
        (9, 13), (13, 14), (14, 15), (15, 16),
        (13, 17), (17, 18), (18, 19), (19, 20),
        (0, 17)
    ]

    def __init__(
        self,
        mode=False,
        maxHands=2,
        detectionCon=0.5,
        trackCon=0.5
    ):

        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = float(detectionCon)
        self.trackCon = float(trackCon)

        # Locate the MediaPipe model.
        self.model_path = (
            Path(__file__).resolve().parent
            / "models"
            / "hand_landmarker.task"
        )

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Hand Landmarker model not found: {self.model_path}\n"
                "Download hand_landmarker.task and place it inside "
                "the models folder."
            )

        # Initialize MediaPipe Tasks API.
        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = (
            mp.tasks.vision.HandLandmarkerOptions
        )
        RunningMode = mp.tasks.vision.RunningMode

        options = HandLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path=str(self.model_path)
            ),
            running_mode=RunningMode.VIDEO,
            num_hands=self.maxHands,
            min_hand_detection_confidence=self.detectionCon,
            min_hand_presence_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )

        self.detector = HandLandmarker.create_from_options(
            options
        )

        self.results = None
        self.current_hands = []
        self.timestamp_ms = 0

    def findHands(self, img, draw=True):

        if img is None:
            raise ValueError("Input image cannot be None.")

        # Convert BGR to RGB.
        imgRGB = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2RGB
        )

        # Create MediaPipe image.
        mpImage = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=imgRGB
        )

        # VIDEO mode requires increasing timestamps.
        current_timestamp = time.monotonic_ns() // 1_000_000

        self.timestamp_ms = max(
            self.timestamp_ms + 1,
            current_timestamp
        )

        # Detect hands.
        self.results = self.detector.detect_for_video(
            mpImage,
            self.timestamp_ms
        )

        self.current_hands = (
            self.results.hand_landmarks or []
        )

        # Draw hand landmarks and connections.
        if draw:

            h, w, _ = img.shape

            for hand in self.current_hands:

                points = []

                for landmark in hand:

                    cx = int(landmark.x * w)
                    cy = int(landmark.y * h)

                    points.append((cx, cy))

                # Draw connections.
                for start, end in self.HAND_CONNECTIONS:

                    cv2.line(
                        img,
                        points[start],
                        points[end],
                        (0, 255, 0),
                        2
                    )

                # Draw landmarks.
                for cx, cy in points:

                    cv2.circle(
                        img,
                        (cx, cy),
                        5,
                        (255, 0, 255),
                        cv2.FILLED
                    )

        return img

    def findPosition(self, img, handNo=0, draw=True):

        lmList = []

        # Validate hand index.
        if (
            handNo < 0
            or handNo >= len(self.current_hands)
        ):
            return lmList

        h, w, _ = img.shape

        hand = self.current_hands[handNo]

        for id, landmark in enumerate(hand):

            cx = int(landmark.x * w)
            cy = int(landmark.y * h)

            lmList.append((id, cx, cy))

            # Highlight fingertips.
            if draw and id in [4, 8, 12, 16, 20]:

                cv2.circle(
                    img,
                    (cx, cy),
                    10,
                    (255, 0, 255),
                    cv2.FILLED
                )

        return lmList

    def close(self):

        if self.detector is not None:
            self.detector.close()
            self.detector = None


# Standalone hand tracking test.
def main():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise RuntimeError("Unable to access webcam.")

    detector = None

    try:

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        detector = HandDetector(
            maxHands=2,
            detectionCon=0.7,
            trackCon=0.7
        )

        pTime = 0

        while True:

            success, img = cap.read()

            if not success or img is None:
                print("Unable to read webcam frame.")
                break

            img = cv2.flip(img, 1)

            img = detector.findHands(img)

            lmList = detector.findPosition(
                img,
                draw=False
            )

            cTime = time.time()

            fps = (
                0 if pTime == 0
                else 1 / (cTime - pTime)
            )

            pTime = cTime

            cv2.putText(
                img,
                f"FPS: {int(fps)}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),
                2
            )

            cv2.putText(
                img,
                f"Hands detected: {len(detector.current_hands)}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.imshow(
                "MediaPipe Hand Tracking",
                img
            )

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            
            if cv2.getWindowProperty(
                "Mediapipe Hand Tracking",
                cv2.WND_PROP_VISIBLE
            ) < 1:
                break

    finally:

        cap.release()

        if detector is not None:
            detector.close()

        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
