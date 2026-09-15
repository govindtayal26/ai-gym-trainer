import cv2
import mediapipe as mp


class PoseDetector:

    def __init__(self):

        self.mp_pose = mp.solutions.pose

        self.mp_drawing = mp.solutions.drawing_utils

        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def detect(self, frame):

        # OpenCV uses BGR
        # MediaPipe expects RGB

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = self.pose.process(
            rgb_frame
        )

        return results

    def draw_landmarks(
        self,
        frame,
        results
    ):

        if results.pose_landmarks:

            self.mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS
            )

        return frame

    def get_landmarks(self, results):

        if results.pose_landmarks is None:
            return None

        return results.pose_landmarks.landmark

    def close(self):

        self.pose.close()