
import numpy as np

from exercises.base_exercise import BaseExercise


class ShoulderPress(BaseExercise):

    def __init__(self):

        super().__init__()

        # ========================================
        # REP SETTINGS
        # ========================================

        self.stage = "down"

        # Arm bent position
        self.down_angle = 90

        # Arm extended position
        self.up_angle = 160

        # Minimum movement required for a valid rep
        self.min_rep_range = 50

        # ========================================
        # ARM STATE
        # ========================================

        self.active_arm = None

        # ========================================
        # ANGLE STATE
        # ========================================

        self.current_angle = 90

        self.angle_history = []

        self.smoothing_window = 5

        self.lowest_angle = 180
        self.highest_angle = 0

        # ========================================
        # FORM SCORES
        # ========================================

        self.range_score = 100
        self.elbow_score = 100
        self.shoulder_score = 100
        self.body_score = 100

        self.form_score = 0

        # ========================================
        # MOVEMENT TRACKING
        # ========================================

        self.previous_angle = None

        self.movement_history = []

        self.max_movement_history = 20

    # ========================================
    # ANGLE CALCULATION
    # ========================================

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

    # ========================================
    # GET POINT
    # ========================================

    def get_point(self, landmarks, index):

        landmark = landmarks[index]

        return [
            landmark.x,
            landmark.y
        ]

    # ========================================
    # GET ARM ANGLES
    # ========================================

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

    # ========================================
    # SELECT ACTIVE ARM
    # ========================================

    def select_active_arm(self, angles):

        if not angles:

            return None

        if self.active_arm in angles:

            return self.active_arm

        return min(
            angles,
            key=angles.get
        )

    # ========================================
    # SMOOTH ANGLE
    # ========================================

    def smooth_angle(self, angle):

        self.angle_history.append(angle)

        if len(self.angle_history) > self.smoothing_window:

            self.angle_history.pop(0)

        return (
            sum(self.angle_history)
            /
            len(self.angle_history)
        )

    # ========================================
    # RANGE SCORE
    # ========================================

    def calculate_range_score(self, angle):

        # Excellent extension
        if angle >= 165:

            return 100

        # Good
        if angle >= 155:

            return 95

        # Slightly incomplete
        if angle >= 145:

            return 85

        # Incomplete
        if angle >= 130:

            return 70

        # Poor
        if angle >= 115:

            return 55

        return 40

    # ========================================
    # ELBOW SCORE
    # ========================================

    def calculate_elbow_score(self, angle):

        # Good pressing range
        if 80 <= angle <= 160:

            return 100

        if 70 <= angle < 80:

            return 90

        if 160 < angle <= 170:

            return 90

        if 60 <= angle < 70:

            return 75

        if 170 < angle <= 175:

            return 75

        return 60

    # ========================================
    # SHOULDER POSITION SCORE
    # ========================================

    def calculate_shoulder_score(self, landmarks):

        if self.active_arm == "left":

            shoulder = landmarks[11]
            elbow = landmarks[13]

        else:

            shoulder = landmarks[12]
            elbow = landmarks[14]

        # Distance between shoulder and elbow
        vertical_distance = abs(
            shoulder.y -
            elbow.y
        )

        horizontal_distance = abs(
            shoulder.x -
            elbow.x
        )

        total_distance = np.sqrt(
            vertical_distance ** 2
            +
            horizontal_distance ** 2
        )

        if total_distance == 0:

            return 50

        horizontal_ratio = (
            horizontal_distance
            /
            total_distance
        )

        # Arm should remain reasonably
        # close to the body's vertical plane.

        if horizontal_ratio <= 0.35:

            return 100

        if horizontal_ratio <= 0.45:

            return 90

        if horizontal_ratio <= 0.55:

            return 75

        if horizontal_ratio <= 0.65:

            return 60

        return 45

    # ========================================
    # BODY SCORE
    # ========================================

    def calculate_body_score(self, landmarks):

        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]

        left_hip = landmarks[23]
        right_hip = landmarks[24]

        shoulder_x = (
            left_shoulder.x
            +
            right_shoulder.x
        ) / 2

        shoulder_y = (
            left_shoulder.y
            +
            right_shoulder.y
        ) / 2

        hip_x = (
            left_hip.x
            +
            right_hip.x
        ) / 2

        hip_y = (
            left_hip.y
            +
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

            return 50

        torso_lean = (
            horizontal_difference
            /
            vertical_difference
        )

        if torso_lean <= 0.15:

            return 100

        if torso_lean <= 0.25:

            return 90

        if torso_lean <= 0.35:

            return 75

        if torso_lean <= 0.45:

            return 60

        return 40

    # ========================================
    # FORM SCORE
    # ========================================

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

        self.elbow_score = (
            self.calculate_elbow_score(
                angle
            )
        )

        self.shoulder_score = (
            self.calculate_shoulder_score(
                landmarks
            )
        )

        self.body_score = (
            self.calculate_body_score(
                landmarks
            )
        )

        score = (

            self.range_score * 0.35

            +

            self.elbow_score * 0.20

            +

            self.shoulder_score * 0.25

            +

            self.body_score * 0.20

        )

        return int(
            round(
                max(
                    0,
                    min(
                        100,
                        score
                    )
                )
            )
        )

    # ========================================
    # FEEDBACK
    # ========================================

    def get_feedback(self, angle):

        # --------------------------------
        # BODY
        # --------------------------------

        if self.body_score < 60:

            return "Keep your body upright"

        # --------------------------------
        # SHOULDER
        # --------------------------------

        if self.shoulder_score < 60:

            return "Keep your elbows controlled"

        # --------------------------------
        # PRESS HIGHER
        # --------------------------------

        if (
            self.stage == "up"
            and
            angle < 145
        ):

            return "Press higher"

        # --------------------------------
        # DON'T OVEREXTEND
        # --------------------------------

        if angle > 175:

            return "Don't lock your elbows"

        # --------------------------------
        # GOOD FORM
        # --------------------------------

        if self.form_score >= 90:

            return "Excellent shoulder press form"

        if self.form_score >= 75:

            return "Good shoulder press form"

        return "Control your movement"

    # ========================================
    # UPDATE
    # ========================================

    def update(self, landmarks):

        # --------------------------------
        # NO POSE
        # --------------------------------

        if landmarks is None:

            self.feedback = "No pose detected"

            self.form_score = 0

            return self.get_result()

        # --------------------------------
        # REQUIRED LANDMARKS
        # --------------------------------

        required_points = [

            11,
            12,
            13,
            14,
            15,
            16,
            23,
            24

        ]

        for index in required_points:

            if landmarks[index].visibility < 0.4:

                self.feedback = (
                    "Keep your upper body visible"
                )

                self.form_score = 0

                return self.get_result()

        # --------------------------------
        # GET ARM ANGLES
        # --------------------------------

        angles = self.get_arm_angles(
            landmarks
        )

        if not angles:

            self.feedback = (
                "Arms not visible"
            )

            self.form_score = 0

            return self.get_result()

        # --------------------------------
        # SELECT ARM
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

        # --------------------------------
        # TRACK RANGE
        # --------------------------------

        self.lowest_angle = min(
            self.lowest_angle,
            angle
        )

        self.highest_angle = max(
            self.highest_angle,
            angle
        )

        # --------------------------------
        # MOVEMENT TRACKING
        # --------------------------------

        if self.previous_angle is not None:

            movement = abs(
                angle -
                self.previous_angle
            )

            self.movement_history.append(
                movement
            )

            if (
                len(self.movement_history)
                >
                self.max_movement_history
            ):

                self.movement_history.pop(0)

        self.previous_angle = angle

        # =================================
        # REP STATE MACHINE
        # =================================

        # Arm is extended
        if angle >= self.up_angle:

            if self.stage == "down":

                movement_range = (
                    self.highest_angle
                    -
                    self.lowest_angle
                )

                if (
                    movement_range
                    >=
                    self.min_rep_range
                ):

                    self.reps += 1

                    print(
                        f"\n"
                        f"SHOULDER PRESS REP: "
                        f"{self.reps}"
                    )

                self.lowest_angle = angle
                self.highest_angle = angle

            self.stage = "up"

        # Arm is bent
        elif angle <= self.down_angle:

            self.stage = "down"

        # =================================
        # FORM ANALYSIS
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
            f"Exercise: Shoulder Press | "
            f"Arm: {self.active_arm} | "
            f"Angle: {angle:6.1f} | "
            f"Stage: {self.stage:4} | "
            f"Range: {self.range_score:3d} | "
            f"Shoulder: {self.shoulder_score:3d} | "
            f"Body: {self.body_score:3d} | "
            f"Score: {self.form_score:3d} | "
            f"Reps: {self.reps}",
            end=""
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

        self.stage = "down"

        self.active_arm = None

        self.current_angle = 90

        self.angle_history = []

        self.lowest_angle = 180

        self.highest_angle = 0

        self.range_score = 100

        self.elbow_score = 100

        self.shoulder_score = 100

        self.body_score = 100

        self.form_score = 0

        self.previous_angle = None

        self.movement_history = []

### Now update `exercise_manager.py`



