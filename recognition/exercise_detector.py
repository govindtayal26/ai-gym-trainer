from recognition.pose_features import PoseFeatures


class ExerciseDetector:

    def __init__(self):

        self.current_exercise = "Unknown"

        # Reusable pose feature calculator
        self.features = PoseFeatures()

    # ====================================
    # BICEP CURL
    # ====================================

    def bicep_score(self, landmarks):

        scores = []

        # --------------------------------
        # LEFT ARM
        # --------------------------------

        if self.features.all_visible(
            landmarks,
            [11, 13, 15]
        ):

            left_angle = (
                self.features.left_elbow_angle(
                    landmarks
                )
            )

            if left_angle < 80:

                scores.append(100)

            elif left_angle < 110:

                scores.append(80)

            elif left_angle < 140:

                scores.append(50)

            else:

                scores.append(20)

        # --------------------------------
        # RIGHT ARM
        # --------------------------------

        if self.features.all_visible(
            landmarks,
            [12, 14, 16]
        ):

            right_angle = (
                self.features.right_elbow_angle(
                    landmarks
                )
            )

            if right_angle < 80:

                scores.append(100)

            elif right_angle < 110:

                scores.append(80)

            elif right_angle < 140:

                scores.append(50)

            else:

                scores.append(20)

        if not scores:

            return 0

        score = (
            sum(scores) /
            len(scores)
        )

        # --------------------------------
        # STANDING POSTURE
        # --------------------------------

        if self.features.all_visible(
            landmarks,
            [23, 25, 27]
        ):

            knee = (
                self.features.left_knee_angle(
                    landmarks
                )
            )

            if knee > 145:

                score += 10

        return min(
            int(score),
            100
        )

    # ====================================
    # SQUAT
    # ====================================

    def squat_score(self, landmarks):

        required = [
            23,
            24,
            25,
            26,
            27,
            28
        ]

        if not self.features.all_visible(
            landmarks,
            required
        ):

            return 0

        knee_angle = (
            self.features.average_knee_angle(
                landmarks
            )
        )

        if knee_angle <= 0:

            return 0

        if knee_angle < 100:

            return 100

        elif knee_angle < 120:

            return 85

        elif knee_angle < 140:

            return 65

        return 20

    # ====================================
    # PUSH-UP
    # ====================================

    def pushup_score(self, landmarks):

        required = [
            11,
            12,
            13,
            14,
            15,
            16,
            23,
            24
        ]

        if not self.features.all_visible(
            landmarks,
            required
        ):

            return 0

        # --------------------------------
        # BODY POSITION
        # --------------------------------

        body_difference = (
            self.features.body_difference(
                landmarks
            )
        )

        # Push-up body should be
        # relatively horizontal.

        if body_difference > 0.30:

            return 0

        # --------------------------------
        # ELBOW ANGLE
        # --------------------------------

        elbow_angle = (
            self.features.average_elbow_angle(
                landmarks
            )
        )

        if elbow_angle <= 0:

            return 0

        if elbow_angle < 100:

            return 100

        elif elbow_angle < 130:

            return 80

        elif elbow_angle < 160:

            return 60

        return 20

    # ====================================
    # SHOULDER PRESS
    # ====================================

    def shoulder_press_score(self, landmarks):

        required = [
            11,
            12,
            13,
            14,
            15,
            16,
            23,
            24
        ]

        if not self.features.all_visible(
            landmarks,
            required
        ):

            return 0

        # --------------------------------
        # TORSO
        # --------------------------------

        torso_height = (
            self.features.torso_height(
                landmarks
            )
        )

        if torso_height < 0.20:

            return 0

        # --------------------------------
        # ELBOW ANGLE
        # --------------------------------

        elbow_angle = (
            self.features.average_elbow_angle(
                landmarks
            )
        )

        if elbow_angle <= 0:

            return 0

        # --------------------------------
        # BASE SCORE
        # --------------------------------

        if elbow_angle <= 100:

            score = 90

        elif elbow_angle <= 120:

            score = 80

        elif elbow_angle <= 140:

            score = 65

        elif elbow_angle <= 160:

            score = 50

        else:

            score = 30

        # --------------------------------
        # WRIST POSITION
        # --------------------------------

        if self.features.wrists_above_shoulders(
            landmarks
        ):

            score += 10

        # --------------------------------
        # STANDING POSTURE
        # --------------------------------

        if torso_height > 0.25:

            score += 5

        return min(
            int(score),
            100
        )

    # ====================================
    # LATERAL RAISE
    # ====================================

    def lateral_raise_score(self, landmarks):

        required = [
            11,
            12,
            13,
            14,
            15,
            16,
            23,
            24
        ]

        if not self.features.all_visible(
            landmarks,
            required
        ):

            return 0

        # --------------------------------
        # SHOULDER ANGLES
        # --------------------------------

        left_angle = self.features.angle(
            landmarks,
            23,
            11,
            13
        )

        right_angle = self.features.angle(
            landmarks,
            24,
            12,
            14
        )

        average_angle = (
            left_angle +
            right_angle
        ) / 2

        # --------------------------------
        # WRIST HEIGHT
        # --------------------------------

        wrist_difference = (
            self.features.wrist_shoulder_difference(
                landmarks
            )
        )

        # --------------------------------
        # BASE SCORE
        # --------------------------------

        if average_angle >= 65:

            score = 85

        elif average_angle >= 50:

            score = 70

        elif average_angle >= 35:

            score = 50

        else:

            score = 20

        # --------------------------------
        # WRISTS ABOVE SHOULDERS
        # --------------------------------

        if wrist_difference > 0.02:

            score += 10

        # --------------------------------
        # ELBOW CONTROL
        # --------------------------------

        left_elbow = (
            self.features.left_elbow_angle(
                landmarks
            )
        )

        right_elbow = (
            self.features.right_elbow_angle(
                landmarks
            )
        )

        if (
            130 <= left_elbow <= 175
            and
            130 <= right_elbow <= 175
        ):

            score += 10

        return min(
            int(score),
            100
        )

    # ====================================
    # MAIN DETECTOR
    # ====================================

    def detect(self, landmarks):

        if landmarks is None:

            self.current_exercise = "Unknown"

            return "Unknown"

        # =================================
        # CALCULATE ALL SCORES
        # =================================

        scores = {

            "Bicep Curl":
                self.bicep_score(
                    landmarks
                ),

            "Squat":
                self.squat_score(
                    landmarks
                ),

            "Push-up":
                self.pushup_score(
                    landmarks
                ),

            "Shoulder Press":
                self.shoulder_press_score(
                    landmarks
                ),

            "Lateral Raise":
                self.lateral_raise_score(
                    landmarks
                )
        }

        # =================================
        # SORT SCORES
        # =================================

        sorted_scores = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True
        )

        best_exercise = (
            sorted_scores[0][0]
        )

        best_score = (
            sorted_scores[0][1]
        )

        second_score = (
            sorted_scores[1][1]
        )

        # =================================
        # CONFIDENCE MARGIN
        # =================================

        score_difference = (
            best_score -
            second_score
        )

        # If confidence is too low,
        # don't select an exercise.

        if best_score < 45:

            self.current_exercise = "Unknown"

            return "Unknown"

        # If two exercises have nearly
        # identical scores, wait for
        # stabilizer instead of making
        # an aggressive decision.

        if score_difference < 8:

            self.current_exercise = "Unknown"

            return "Unknown"

        # =================================
        # UPDATE CURRENT EXERCISE
        # =================================

        self.current_exercise = (
            best_exercise
        )

        # =================================
        # DEBUG OUTPUT
        # =================================

        print(
            f"\r"
            f"Bicep: "
            f"{scores['Bicep Curl']:3} | "
            f"Squat: "
            f"{scores['Squat']:3} | "
            f"Push-up: "
            f"{scores['Push-up']:3} | "
            f"Shoulder: "
            f"{scores['Shoulder Press']:3} | "
            f"Lateral: "
            f"{scores['Lateral Raise']:3} | "
            f"Detected: "
            f"{best_exercise}",
            end=""
        )

        return best_exercise

    # ====================================
    # GET CURRENT EXERCISE
    # ====================================

    def get_current_exercise(self):

        return self.current_exercise

    # ====================================
    # GET ALL SCORES
    # ====================================

    def get_scores(self, landmarks):

        if landmarks is None:

            return {

                "Bicep Curl": 0,

                "Squat": 0,

                "Push-up": 0,

                "Shoulder Press": 0,

                "Lateral Raise": 0
            }

        return {

            "Bicep Curl":
                self.bicep_score(
                    landmarks
                ),

            "Squat":
                self.squat_score(
                    landmarks
                ),

            "Push-up":
                self.pushup_score(
                    landmarks
                ),

            "Shoulder Press":
                self.shoulder_press_score(
                    landmarks
                ),

            "Lateral Raise":
                self.lateral_raise_score(
                    landmarks
                )
        }