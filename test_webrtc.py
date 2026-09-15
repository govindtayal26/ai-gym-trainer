import cv2
import streamlit as st

from streamlit_webrtc import webrtc_streamer, WebRtcMode

from pose_detector import PoseDetector
from recognition.exercise_detector import ExerciseDetector


# ============================================================
# STREAMLIT CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Gym Trainer",
    layout="wide"
)

st.title("🏋️ AI Gym Trainer")
st.write("Stage 5 — Automatic Exercise Detection")


# ============================================================
# VIDEO PROCESSOR
# ============================================================

class VideoProcessor:

    def __init__(self):

        # ----------------------------------------
        # Pose Detection
        # ----------------------------------------

        self.pose_detector = PoseDetector()

        # ----------------------------------------
        # Exercise Detection
        # ----------------------------------------

        self.exercise_detector = ExerciseDetector()

        # ----------------------------------------
        # Frame Counter
        # ----------------------------------------

        self.frame_count = 0

    def recv(self, frame):

        # ====================================================
        # 1. WEBRTC → OPENCV
        # ====================================================

        image = frame.to_ndarray(format="bgr24")

        # Mirror camera
        image = cv2.flip(image, 1)

        # ====================================================
        # 2. POSE DETECTION
        # ====================================================

        results = self.pose_detector.detect(image)

        # ====================================================
        # 3. DRAW SKELETON
        # ====================================================

        image = self.pose_detector.draw_landmarks(
            image,
            results
        )

        # ====================================================
        # 4. GET LANDMARKS
        # ====================================================

        landmarks = self.pose_detector.get_landmarks(
            results
        )

        # ====================================================
        # 5. EXERCISE DETECTION
        # ====================================================

        if landmarks is not None:

            detected_exercise = (
                self.exercise_detector.detect(
                    landmarks
                )
            )

        else:

            detected_exercise = "Unknown"

        # ====================================================
        # 6. DISPLAY
        # ====================================================

        if landmarks is not None:

            cv2.putText(
                image,
                "PERSON DETECTED",
                (30, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                image,
                f"Exercise: {detected_exercise}",
                (30, 85),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 0),
                2
            )

        else:

            cv2.putText(
                image,
                "NO PERSON DETECTED",
                (30, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

            cv2.putText(
                image,
                "Exercise: Unknown",
                (30, 85),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 0),
                2
            )

        # ====================================================
        # 7. RETURN FRAME
        # ====================================================

        return frame.from_ndarray(
            image,
            format="bgr24"
        )


# ============================================================
# WEBRTC
# ============================================================

webrtc_streamer(
    key="gym-camera",

    mode=WebRtcMode.SENDRECV,

    video_processor_factory=VideoProcessor,

    media_stream_constraints={
        "video": True,
        "audio": False,
    },
)