
import numpy as np

from exercises.base_exercise import BaseExercise


class BicepCurl(BaseExercise):

    def __init__(self):

        super().__init__()

        # ====================================
        # REP SETTINGS
        # ====================================

        self.stage = "down"

        self.down_angle = 150
        self.up_angle = 80

        # ====================================
        # ARM
        # ====================================

        self.active_arm = None

        # ====================================
        # ANGLE
        # ====================================

        self.current_angle = 180

        self.angle_history = []

        self.smoothing_window = 5

        # ====================================
        # REP PROTECTION
        # ====================================

        self.min_rep_angle_difference = 50

        self.lowest_angle = 180
        self.highest_angle = 0

        # ====================================
        # FORM ANALYSIS
        # ====================================

        self.elbow_reference_y = None

        self.elbow_movement_history = []

        self.max_elbow_movement = 0.08

        self.minimum_curl_angle = 100

        self.full_extension_angle = 150

        # ====================================
        # FORM SCORES
        # ====================================

        self.range_score = 100
        self.elbow_score = 100
        self.extension_score = 100

    # ====================================
    # ANGLE CALCULATION
    # ====================================

    def calculate_angle(self, a, b, c):

        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        ba = a - b
        bc = c - b

        denominator = (
            np.linalg.norm(ba)
            *
            np.linalg.norm(bc)
        )

        if denominator == 0:

            return 180

        cosine_angle = (
            np.dot(ba, bc)
            /
            denominator
        )

        cosine_angle = np.clip(
            cosine_angle,
            -1.0,
            1.0
        )

        angle = np.degrees(
            np.arccos(
                cosine_angle
            )
        )

        return angle

    # ====================================
    # GET POINT
    # ====================================

    def get_point(self, landmarks, index):

        landmark = landmarks[index]

        return [
            landmark.x,
            landmark.y
        ]

    # ====================================
    # GET ARM ANGLES
    # ====================================

    def get_arm_angles(self, landmarks):

        angles = {}

        # --------------------------------
        # LEFT ARM
        # --------------------------------

        if (
            landmarks[11].visibility > 0.4
            and
            landmarks[13].visibility > 0.4
            and
            landmarks[15].visibility > 0.4
        ):

            left_angle = self.calculate_angle(

                self.get_point(
                    landmarks,
                    11
                ),

                self.get_point(
                    landmarks,
                    13
                ),

                self.get_point(
                    landmarks,
                    15
                )
            )

            angles["left"] = left_angle

        # --------------------------------
        # RIGHT ARM
        # --------------------------------

        if (
            landmarks[12].visibility > 0.4
            and
            landmarks[14].visibility > 0.4
            and
            landmarks[16].visibility > 0.4
        ):

            right_angle = self.calculate_angle(

                self.get_point(
                    landmarks,
                    12
                ),

                self.get_point(
                    landmarks,
                    14
                ),

                self.get_point(
                    landmarks,
                    16
                )
            )

            angles["right"] = right_angle

        return angles

    # ====================================
    # SELECT ACTIVE ARM
    # ====================================

    def select_active_arm(self, angles):

        if not angles:

            return None

        if self.active_arm in angles:

            return self.active_arm

        return min(
            angles,
            key=angles.get
        )

    # ====================================
    # SMOOTH ANGLE
    # ====================================

    def smooth_angle(self, angle):

        self.angle_history.append(
            angle
        )

        if (
            len(self.angle_history)
            >
            self.smoothing_window
        ):

            self.angle_history.pop(0)

        return (
            sum(self.angle_history)
            /
            len(self.angle_history)
        )

    # ====================================
    # ELBOW STABILITY
    # ====================================

    def calculate_elbow_score(
        self,
        landmarks
    ):

        if self.active_arm == "left":

            elbow_index = 13

        else:

            elbow_index = 14

        elbow = landmarks[
            elbow_index
        ]

        elbow_y = elbow.y

        # --------------------------------
        # FIRST FRAME
        # --------------------------------

        if self.elbow_reference_y is None:

            self.elbow_reference_y = (
                elbow_y
            )

            return 100

        # --------------------------------
        # MOVEMENT
        # --------------------------------

        movement = abs(
            elbow_y
            -
            self.elbow_reference_y
        )

        self.elbow_movement_history.append(
            movement
        )

        if (
            len(
                self.elbow_movement_history
            )
            >
            20
        ):

            self.elbow_movement_history.pop(
                0
            )

        # --------------------------------
        # SCORE
        # --------------------------------

        if movement <= 0.03:

            return 100

        if movement <= 0.05:

            return 90

        if movement <= 0.08:

            return 75

        if movement <= 0.12:

            return 60

        return 40

    # ====================================
    # RANGE SCORE
    # ====================================

    def calculate_range_score(
        self,
        angle
    ):

        # Excellent curl

        if angle <= 80:

            return 100

        # Good

        if angle <= 90:

            return 95

        # Slightly incomplete

        if angle <= 100:

            return 85

        # Incomplete

        if angle <= 115:

            return 70

        # Very incomplete

        return 50

    # ====================================
    # EXTENSION SCORE
    # ====================================

    def calculate_extension_score(
        self,
        angle
    ):

        if angle >= 160:

            return 100

        if angle >= 150:

            return 95

        if angle >= 140:

            return 85

        if angle >= 130:

            return 70

        return 55

    # ====================================
    # FINAL FORM SCORE
    # ====================================

    def calculate_form_score(
        self,
        angle,
        landmarks
    ):

        self.range_score = (
            self.calculate_range_score(
                angle
            )
        )

        self.extension_score = (
            self.calculate_extension_score(
                angle
            )
        )

        self.elbow_score = (
            self.calculate_elbow_score(
                landmarks
            )
        )

        score = (

            self.range_score * 0.40

            +

            self.elbow_score * 0.40

            +

            self.extension_score * 0.20
        )

        return int(
            round(score)
        )

    # ====================================
    # FEEDBACK
    # ====================================

    def get_feedback(
        self,
        angle
    ):

        # --------------------------------
        # ELBOW
        # --------------------------------

        if self.elbow_score < 60:

            return (
                "Keep your elbow stable"
            )

        # --------------------------------
        # CURL RANGE
        # --------------------------------

        if (
            self.stage == "up"
            and
            angle > 100
        ):

            return (
                "Curl higher"
            )

        # --------------------------------
        # EXTENSION
        # --------------------------------

        if (
            self.stage == "down"
            and
            angle < 140
        ):

            return (
                "Extend your arm"
            )

        # --------------------------------
        # OVER CURL
        # --------------------------------

        if angle < 55:

            return (
                "Don't curl too far"
            )

        # --------------------------------
        # GOOD
        # --------------------------------

        if self.form_score >= 90:

            return (
                "Excellent form"
            )

        if self.form_score >= 75:

            return (
                "Good form"
            )

        return (
            "Keep your movement controlled"
        )

    # ====================================
    # UPDATE
    # ====================================

    def update(self, landmarks):

        # --------------------------------
        # NO POSE
        # --------------------------------

        if landmarks is None:

            self.feedback = (
                "No pose detected"
            )

            self.form_score = 0

            return self.get_result()

        # --------------------------------
        # ARM ANGLES
        # --------------------------------

        angles = (
            self.get_arm_angles(
                landmarks
            )
        )

        if not angles:

            self.feedback = (
                "Arms not visible"
            )

            self.form_score = 0

            return self.get_result()

        # --------------------------------
        # ACTIVE ARM
        # --------------------------------

        self.active_arm = (
            self.select_active_arm(
                angles
            )
        )

        angle = angles[
            self.active_arm
        ]

        # --------------------------------
        # SMOOTH
        # --------------------------------

        angle = self.smooth_angle(
            angle
        )

        self.current_angle = angle

        # =================================
        # TRACK RANGE
        # =================================

        self.lowest_angle = min(
            self.lowest_angle,
            angle
        )

        self.highest_angle = max(
            self.highest_angle,
            angle
        )

        # =================================
        # REP STATE MACHINE
        # =================================

        if angle >= self.down_angle:

            self.stage = "down"

        elif angle <= self.up_angle:

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
                        f"\n"
                        f"BICEP REP: "
                        f"{self.reps}"
                    )

                self.lowest_angle = angle
                self.highest_angle = angle

            self.stage = "up"

        # =================================
        # FORM SCORE
        # =================================

        self.form_score = (
            self.calculate_form_score(
                angle,
                landmarks
            )
        )

        # =================================
        # FEEDBACK
        # =================================

        self.feedback = (
            self.get_feedback(
                angle
            )
        )

        # =================================
        # DEBUG
        # =================================

        print(
            f"\r"
            f"Arm: {self.active_arm} | "
            f"Angle: {angle:6.1f} | "
            f"Stage: {self.stage} | "
            f"Score: {self.form_score:3d} | "
            f"Reps: {self.reps}",
            end=""
        )

        return self.get_result()

    # ====================================
    # RESET
    # ====================================

    def reset(self):

        super().reset()

        self.stage = "down"

        self.active_arm = None

        self.current_angle = 180

        self.angle_history = []

        self.lowest_angle = 180

        self.highest_angle = 0

        self.elbow_reference_y = None

        self.elbow_movement_history = []

        self.range_score = 100

        self.elbow_score = 100

        self.extension_score = 100
