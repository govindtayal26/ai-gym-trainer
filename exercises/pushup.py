
import numpy as np

from exercises.base_exercise import BaseExercise


class PushUp(BaseExercise):

    def __init__(self):

        super().__init__()

        # ====================================
        # REP SETTINGS
        # ====================================

        self.stage = "up"

        self.up_angle = 160
        self.down_angle = 95

        # ====================================
        # ANGLE SMOOTHING
        # ====================================

        self.angle_history = []

        self.smoothing_window = 5

        self.current_angle = 180

        # ====================================
        # REP PROTECTION
        # ====================================

        self.highest_angle = 180
        self.lowest_angle = 180

        self.min_rep_range = 45

        # ====================================
        # FORM SCORES
        # ====================================

        self.depth_score = 100
        self.body_alignment_score = 100
        self.elbow_score = 100

        # ====================================
        # BODY ALIGNMENT
        # ====================================

        self.body_alignment_history = []

    # ====================================
    # ANGLE CALCULATION
    # ====================================

    def calculate_angle(
        self,
        a,
        b,
        c
    ):

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
    # GET LANDMARK
    # ====================================

    def get_landmark(
        self,
        landmarks,
        index
    ):

        landmark = landmarks[index]

        return [
            landmark.x,
            landmark.y
        ]

    # ====================================
    # SMOOTH ANGLE
    # ====================================

    def smooth_angle(
        self,
        angle
    ):

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
    # ELBOW ANGLE
    # ====================================

    def get_elbow_angle(
        self,
        landmarks
    ):

        LEFT_SHOULDER = 11
        LEFT_ELBOW = 13
        LEFT_WRIST = 15

        RIGHT_SHOULDER = 12
        RIGHT_ELBOW = 14
        RIGHT_WRIST = 16

        left_angle = self.calculate_angle(

            self.get_landmark(
                landmarks,
                LEFT_SHOULDER
            ),

            self.get_landmark(
                landmarks,
                LEFT_ELBOW
            ),

            self.get_landmark(
                landmarks,
                LEFT_WRIST
            )
        )

        right_angle = self.calculate_angle(

            self.get_landmark(
                landmarks,
                RIGHT_SHOULDER
            ),

            self.get_landmark(
                landmarks,
                RIGHT_ELBOW
            ),

            self.get_landmark(
                landmarks,
                RIGHT_WRIST
            )
        )

        return (
            left_angle
            +
            right_angle
        ) / 2

    # ====================================
    # DEPTH SCORE
    # ====================================

    def calculate_depth_score(
        self,
        angle
    ):

        if angle <= 80:

            return 100

        if angle <= 95:

            return 95

        if angle <= 105:

            return 90

        if angle <= 120:

            return 75

        if angle <= 140:

            return 60

        return 40

    # ====================================
    # BODY ALIGNMENT
    # ====================================

    def calculate_body_alignment(
        self,
        landmarks
    ):

        # --------------------------------
        # Shoulder
        # --------------------------------

        shoulder_x = (
            landmarks[11].x
            +
            landmarks[12].x
        ) / 2

        shoulder_y = (
            landmarks[11].y
            +
            landmarks[12].y
        ) / 2

        # --------------------------------
        # Hip
        # --------------------------------

        hip_x = (
            landmarks[23].x
            +
            landmarks[24].x
        ) / 2

        hip_y = (
            landmarks[23].y
            +
            landmarks[24].y
        ) / 2

        # --------------------------------
        # Ankle
        # --------------------------------

        ankle_x = (
            landmarks[27].x
            +
            landmarks[28].x
        ) / 2

        ankle_y = (
            landmarks[27].y
            +
            landmarks[28].y
        ) / 2

        # --------------------------------
        # Body line
        # --------------------------------

        body_vector_x = (
            ankle_x
            -
            shoulder_x
        )

        body_vector_y = (
            ankle_y
            -
            shoulder_y
        )

        body_length = np.sqrt(
            body_vector_x ** 2
            +
            body_vector_y ** 2
        )

        if body_length == 0:

            return 50

        # --------------------------------
        # Distance of hip from
        # shoulder-ankle line
        # --------------------------------

        numerator = abs(

            body_vector_x
            *
            (
                shoulder_y
                -
                hip_y
            )

            -

            (
                shoulder_x
                -
                hip_x
            )
            *
            body_vector_y
        )

        distance = (
            numerator
            /
            body_length
        )

        # --------------------------------
        # SCORE
        # --------------------------------

        if distance <= 0.03:

            return 100

        if distance <= 0.05:

            return 90

        if distance <= 0.08:

            return 75

        if distance <= 0.12:

            return 60

        return 40

    # ====================================
    # ELBOW SCORE
    # ====================================

    def calculate_elbow_score(
        self,
        angle
    ):

        if 70 <= angle <= 130:

            return 100

        if 60 <= angle < 70:

            return 90

        if 130 < angle <= 150:

            return 90

        if 45 <= angle < 60:

            return 75

        if 150 < angle <= 165:

            return 75

        return 60

    # ====================================
    # FINAL FORM SCORE
    # ====================================

    def calculate_form_score(
        self,
        angle,
        landmarks
    ):

        self.depth_score = (
            self.calculate_depth_score(
                angle
            )
        )

        self.body_alignment_score = (
            self.calculate_body_alignment(
                landmarks
            )
        )

        self.elbow_score = (
            self.calculate_elbow_score(
                angle
            )
        )

        score = (

            self.depth_score * 0.45

            +

            self.body_alignment_score * 0.35

            +

            self.elbow_score * 0.20
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
        # BODY ALIGNMENT
        # --------------------------------

        if self.body_alignment_score < 60:

            return (
                "Keep your body straight"
            )

        # --------------------------------
        # DEPTH
        # --------------------------------

        if (
            self.stage == "down"
            and
            angle > 120
        ):

            return (
                "Go lower"
            )

        # --------------------------------
        # ELBOWS
        # --------------------------------

        if angle > 150:

            return (
                "Bend your elbows"
            )

        # --------------------------------
        # TOO DEEP
        # --------------------------------

        if angle < 45:

            return (
                "Don't go too low"
            )

        # --------------------------------
        # SCORE
        # --------------------------------

        if self.form_score >= 90:

            return (
                "Excellent push-up form"
            )

        if self.form_score >= 75:

            return (
                "Good push-up form"
            )

        return (
            "Keep your movement controlled"
        )

    # ====================================
    # UPDATE
    # ====================================

    def update(
        self,
        landmarks
    ):

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
            24,
            27,
            28
        ]

        for index in required_points:

            if (
                landmarks[index].visibility
                <
                0.4
            ):

                self.feedback = (
                    "Full body not visible"
                )

                self.form_score = 0

                return self.get_result()

        # =================================
        # ELBOW ANGLE
        # =================================

        elbow_angle = (
            self.get_elbow_angle(
                landmarks
            )
        )

        # --------------------------------
        # SMOOTH
        # --------------------------------

        elbow_angle = (
            self.smooth_angle(
                elbow_angle
            )
        )

        self.current_angle = (
            elbow_angle
        )

        # =================================
        # TRACK MOVEMENT
        # =================================

        self.highest_angle = max(
            self.highest_angle,
            elbow_angle
        )

        self.lowest_angle = min(
            self.lowest_angle,
            elbow_angle
        )

        # =================================
        # REP STATE MACHINE
        # =================================

        if elbow_angle >= self.up_angle:

            self.stage = "up"

        elif elbow_angle <= self.down_angle:

            if self.stage == "up":

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
                        f"PUSH-UP REP: "
                        f"{self.reps}"
                    )

                self.highest_angle = (
                    elbow_angle
                )

                self.lowest_angle = (
                    elbow_angle
                )

            self.stage = "down"

        # =================================
        # FORM
        # =================================

        self.form_score = (
            self.calculate_form_score(
                elbow_angle,
                landmarks
            )
        )

        # =================================
        # FEEDBACK
        # =================================

        self.feedback = (
            self.get_feedback(
                elbow_angle
            )
        )

        # =================================
        # DEBUG
        # =================================

        print(
            f"\r"
            f"Exercise: Push-up | "
            f"Elbow: {elbow_angle:6.1f} | "
            f"Stage: {self.stage} | "
            f"Depth: {self.depth_score:3d} | "
            f"Body: {self.body_alignment_score:3d} | "
            f"Elbow: {self.elbow_score:3d} | "
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

        self.stage = "up"

        self.angle_history = []

        self.current_angle = 180

        self.highest_angle = 180

        self.lowest_angle = 180

        self.depth_score = 100

        self.body_alignment_score = 100

        self.elbow_score = 100

        self.body_alignment_history = []

