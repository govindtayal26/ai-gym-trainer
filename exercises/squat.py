
import numpy as np

from exercises.base_exercise import BaseExercise


class Squat(BaseExercise):

    def __init__(self):

        super().__init__()

        # --------------------------------
        # REP SETTINGS
        # --------------------------------

        self.stage = "up"

        self.up_angle = 165

        self.down_angle = 100

        self.min_rep_angle_difference = 40

        # --------------------------------
        # ANGLE STATE
        # --------------------------------

        self.current_angle = 180

        self.angle_history = []

        self.smoothing_window = 5

        self.lowest_angle = 180

        self.highest_angle = 0

        # --------------------------------
        # FORM ANALYSIS
        # --------------------------------

        self.depth_score = 100

        self.knee_score = 100

        self.torso_score = 100

        self.form_score = 0

    # ========================================
    # CALCULATE ANGLE
    # ========================================

    def calculate_angle(
        self,
        a,
        b,
        c
    ):

        a = np.array(a)

        b = np.array(b)

        c = np.array(c)

        radians = np.arctan2(
            c[1] - b[1],
            c[0] - b[0]
        ) - np.arctan2(
            a[1] - b[1],
            a[0] - b[0]
        )

        angle = np.abs(
            radians * 180.0 / np.pi
        )

        if angle > 180:

            angle = 360 - angle

        return angle

    # ========================================
    # GET POINT
    # ========================================

    def get_point(
        self,
        landmarks,
        index
    ):

        landmark = landmarks[index]

        return [
            landmark.x,
            landmark.y
        ]

    # ========================================
    # SMOOTH ANGLE
    # ========================================

    def smooth_angle(
        self,
        angle
    ):

        self.angle_history.append(
            angle
        )

        if len(self.angle_history) > self.smoothing_window:

            self.angle_history.pop(0)

        return np.mean(
            self.angle_history
        )

    # ========================================
    # KNEE ANGLE
    # ========================================

    def get_knee_angles(
        self,
        landmarks
    ):

        left_hip = self.get_point(
            landmarks,
            23
        )

        left_knee = self.get_point(
            landmarks,
            25
        )

        left_ankle = self.get_point(
            landmarks,
            27
        )

        right_hip = self.get_point(
            landmarks,
            24
        )

        right_knee = self.get_point(
            landmarks,
            26
        )

        right_ankle = self.get_point(
            landmarks,
            28
        )

        left_angle = self.calculate_angle(
            left_hip,
            left_knee,
            left_ankle
        )

        right_angle = self.calculate_angle(
            right_hip,
            right_knee,
            right_ankle
        )

        return left_angle, right_angle

    # ========================================
    # DEPTH SCORE
    # ========================================

    def calculate_depth_score(
        self,
        angle
    ):

        if angle <= 90:

            return 100

        if angle <= 100:

            return 95

        if angle <= 110:

            return 85

        if angle <= 120:

            return 70

        if angle <= 130:

            return 55

        return 40

    # ========================================
    # KNEE ALIGNMENT SCORE
    # ========================================

    def calculate_knee_score(
        self,
        landmarks
    ):

        left_knee = landmarks[25]

        right_knee = landmarks[26]

        left_ankle = landmarks[27]

        right_ankle = landmarks[28]

        left_difference = abs(
            left_knee.x -
            left_ankle.x
        )

        right_difference = abs(
            right_knee.x -
            right_ankle.x
        )

        average_difference = (
            left_difference +
            right_difference
        ) / 2

        if average_difference <= 0.03:

            return 100

        if average_difference <= 0.06:

            return 90

        if average_difference <= 0.09:

            return 75

        if average_difference <= 0.12:

            return 60

        return 40

    # ========================================
    # TORSO SCORE
    # ========================================

    def calculate_torso_score(
        self,
        landmarks
    ):

        left_shoulder = landmarks[11]

        right_shoulder = landmarks[12]

        left_hip = landmarks[23]

        right_hip = landmarks[24]

        shoulder_x = (
            left_shoulder.x +
            right_shoulder.x
        ) / 2

        shoulder_y = (
            left_shoulder.y +
            right_shoulder.y
        ) / 2

        hip_x = (
            left_hip.x +
            right_hip.x
        ) / 2

        hip_y = (
            left_hip.y +
            right_hip.y
        ) / 2

        horizontal_difference = abs(
            shoulder_x -
            hip_x
        )

        vertical_difference = abs(
            shoulder_y -
            hip_y
        )

        if vertical_difference == 0:

            return 100

        torso_lean = (
            horizontal_difference
            /
            vertical_difference
        )

        if torso_lean <= 0.20:

            return 100

        if torso_lean <= 0.30:

            return 90

        if torso_lean <= 0.40:

            return 75

        if torso_lean <= 0.50:

            return 60

        return 40

    # ========================================
    # FORM SCORE
    # ========================================

    def calculate_form_score(self):

        score = (

            self.depth_score * 0.50

            +

            self.knee_score * 0.25

            +

            self.torso_score * 0.25

        )

        return int(
            max(
                0,
                min(
                    100,
                    score
                )
            )
        )

    # ========================================
    # FEEDBACK
    # ========================================

    def generate_feedback(self):

        if self.knee_score < 70:

            return "Keep your knees aligned"

        if self.depth_score < 70:

            return "Go deeper"

        if self.torso_score < 70:

            return "Keep your chest up"

        if self.form_score >= 90:

            return "Excellent squat form"

        if self.form_score >= 75:

            return "Good form"

        return "Control your squat"

    # ========================================
    # UPDATE
    # ========================================

    def update(
        self,
        landmarks
    ):

        if landmarks is None:

            self.feedback = "No person detected"

            return self.get_result()

        # --------------------------------
        # CHECK LANDMARK VISIBILITY
        # --------------------------------

        required_landmarks = [
            23,
            24,
            25,
            26,
            27,
            28
        ]

        for index in required_landmarks:

            if landmarks[index].visibility < 0.5:

                self.feedback = (
                    "Move so your full body is visible"
                )

                return self.get_result()

        # --------------------------------
        # GET KNEE ANGLES
        # --------------------------------

        left_angle, right_angle = (
            self.get_knee_angles(
                landmarks
            )
        )

        average_angle = (
            left_angle +
            right_angle
        ) / 2

        self.current_angle = (
            self.smooth_angle(
                average_angle
            )
        )

        # --------------------------------
        # TRACK RANGE
        # --------------------------------

        self.lowest_angle = min(
            self.lowest_angle,
            self.current_angle
        )

        self.highest_angle = max(
            self.highest_angle,
            self.current_angle
        )

        # --------------------------------
        # FORM ANALYSIS
        # --------------------------------

        self.depth_score = (
            self.calculate_depth_score(
                self.current_angle
            )
        )

        self.knee_score = (
            self.calculate_knee_score(
                landmarks
            )
        )

        self.torso_score = (
            self.calculate_torso_score(
                landmarks
            )
        )

        self.form_score = (
            self.calculate_form_score()
        )

        self.feedback = (
            self.generate_feedback()
        )

        # --------------------------------
        # REP DETECTION
        # --------------------------------

        if self.current_angle >= self.up_angle:

            if self.stage == "down":

                movement_range = (
                    self.highest_angle
                    -
                    self.lowest_angle
                )

                if (
                    movement_range
                    >=
                    self.min_rep_angle_difference
                ):

                    self.reps += 1

                    print(
                        f"SQUAT REP: "
                        f"{self.reps}"
                    )

                self.lowest_angle = (
                    self.current_angle
                )

                self.highest_angle = (
                    self.current_angle
                )

            self.stage = "up"

        elif self.current_angle <= self.down_angle:

            self.stage = "down"

        # --------------------------------
        # DEBUG
        # --------------------------------

        print(
            f"Squat | "
            f"Knee: {self.current_angle:6.1f} | "
            f"Stage: {self.stage:4} | "
            f"Depth: {self.depth_score:3} | "
            f"Knee: {self.knee_score:3} | "
            f"Torso: {self.torso_score:3} | "
            f"Score: {self.form_score:3} | "
            f"Reps: {self.reps}"
        )

        return self.get_result()

    # ========================================
    # RESULT
    # ========================================

    def get_result(self):

        return {

            "reps":
                self.reps,

            "stage":
                self.stage,

            "form_score":
                self.form_score,

            "feedback":
                self.feedback
        }

    # ========================================
    # RESET
    # ========================================

    def reset(self):

        super().reset()

        self.stage = "up"

        self.current_angle = 180

        self.angle_history = []

        self.lowest_angle = 180

        self.highest_angle = 0

        self.depth_score = 100

        self.knee_score = 100

        self.torso_score = 100

        self.form_score = 0

