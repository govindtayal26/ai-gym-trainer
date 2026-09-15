import numpy as np


class PoseFeatures:

    def __init__(self):
        pass

    # ========================================
    # POINT
    # ========================================

    def point(self, landmarks, index):

        landmark = landmarks[index]

        return np.array([
            landmark.x,
            landmark.y
        ])

    # ========================================
    # DISTANCE
    # ========================================

    def distance(self, landmarks, index1, index2):

        point1 = self.point(
            landmarks,
            index1
        )

        point2 = self.point(
            landmarks,
            index2
        )

        return np.linalg.norm(
            point1 - point2
        )

    # ========================================
    # ANGLE
    # ========================================

    def angle(
        self,
        landmarks,
        first,
        middle,
        last
    ):

        a = self.point(
            landmarks,
            first
        )

        b = self.point(
            landmarks,
            middle
        )

        c = self.point(
            landmarks,
            last
        )

        ba = a - b
        bc = c - b

        denominator = (
            np.linalg.norm(ba)
            *
            np.linalg.norm(bc)
        )

        if denominator == 0:

            return 0.0

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

        return float(
            np.degrees(
                np.arccos(
                    cosine_angle
                )
            )
        )

    # ========================================
    # VISIBILITY
    # ========================================

    def visible(
        self,
        landmarks,
        index,
        threshold=0.4
    ):

        return (
            landmarks[index].visibility
            >= threshold
        )

    # ========================================
    # ALL VISIBLE
    # ========================================

    def all_visible(
        self,
        landmarks,
        indexes,
        threshold=0.4
    ):

        for index in indexes:

            if not self.visible(
                landmarks,
                index,
                threshold
            ):

                return False

        return True

    # ========================================
    # AVERAGE POINT
    # ========================================

    def average_point(
        self,
        landmarks,
        indexes
    ):

        points = []

        for index in indexes:

            if self.visible(
                landmarks,
                index
            ):

                points.append(
                    self.point(
                        landmarks,
                        index
                    )
                )

        if not points:

            return np.array([
                0.0,
                0.0
            ])

        return np.mean(
            points,
            axis=0
        )

    # ========================================
    # AVERAGE ANGLE
    # ========================================

    def average_angle(
        self,
        landmarks,
        angle_definitions
    ):

        angles = []

        for first, middle, last in angle_definitions:

            if (
                self.visible(
                    landmarks,
                    first
                )
                and
                self.visible(
                    landmarks,
                    middle
                )
                and
                self.visible(
                    landmarks,
                    last
                )
            ):

                value = self.angle(
                    landmarks,
                    first,
                    middle,
                    last
                )

                angles.append(value)

        if not angles:

            return 0.0

        return float(
            sum(angles)
            /
            len(angles)
        )

    # ========================================
    # LEFT ELBOW ANGLE
    # ========================================

    def left_elbow_angle(
        self,
        landmarks
    ):

        if not self.all_visible(
            landmarks,
            [11, 13, 15]
        ):

            return 0.0

        return self.angle(
            landmarks,
            11,
            13,
            15
        )

    # ========================================
    # RIGHT ELBOW ANGLE
    # ========================================

    def right_elbow_angle(
        self,
        landmarks
    ):

        if not self.all_visible(
            landmarks,
            [12, 14, 16]
        ):

            return 0.0

        return self.angle(
            landmarks,
            12,
            14,
            16
        )

    # ========================================
    # AVERAGE ELBOW ANGLE
    # ========================================

    def average_elbow_angle(
        self,
        landmarks
    ):

        angles = []

        left = self.left_elbow_angle(
            landmarks
        )

        right = self.right_elbow_angle(
            landmarks
        )

        if left > 0:

            angles.append(left)

        if right > 0:

            angles.append(right)

        if not angles:

            return 0.0

        return float(
            sum(angles)
            /
            len(angles)
        )

    # ========================================
    # LEFT KNEE ANGLE
    # ========================================

    def left_knee_angle(
        self,
        landmarks
    ):

        if not self.all_visible(
            landmarks,
            [23, 25, 27]
        ):

            return 0.0

        return self.angle(
            landmarks,
            23,
            25,
            27
        )

    # ========================================
    # RIGHT KNEE ANGLE
    # ========================================

    def right_knee_angle(
        self,
        landmarks
    ):

        if not self.all_visible(
            landmarks,
            [24, 26, 28]
        ):

            return 0.0

        return self.angle(
            landmarks,
            24,
            26,
            28
        )

    # ========================================
    # AVERAGE KNEE ANGLE
    # ========================================

    def average_knee_angle(
        self,
        landmarks
    ):

        angles = []

        left = self.left_knee_angle(
            landmarks
        )

        right = self.right_knee_angle(
            landmarks
        )

        if left > 0:

            angles.append(left)

        if right > 0:

            angles.append(right)

        if not angles:

            return 0.0

        return float(
            sum(angles)
            /
            len(angles)
        )

    # ========================================
    # SHOULDER Y
    # ========================================

    def shoulder_y(
        self,
        landmarks
    ):

        return (
            landmarks[11].y
            +
            landmarks[12].y
        ) / 2

    # ========================================
    # HIP Y
    # ========================================

    def hip_y(
        self,
        landmarks
    ):

        return (
            landmarks[23].y
            +
            landmarks[24].y
        ) / 2

    # ========================================
    # WRIST Y
    # ========================================

    def wrist_y(
        self,
        landmarks
    ):

        return (
            landmarks[15].y
            +
            landmarks[16].y
        ) / 2

    # ========================================
    # TORSO HEIGHT
    # ========================================

    def torso_height(
        self,
        landmarks
    ):

        return abs(
            self.shoulder_y(
                landmarks
            )
            -
            self.hip_y(
                landmarks
            )
        )

    # ========================================
    # BODY DIFFERENCE
    # ========================================

    def body_difference(
        self,
        landmarks
    ):

        return abs(
            self.shoulder_y(
                landmarks
            )
            -
            self.hip_y(
                landmarks
            )
        )

    # ========================================
    # WRIST ABOVE SHOULDER
    # ========================================

    def wrists_above_shoulders(
        self,
        landmarks
    ):

        wrist_y = self.wrist_y(
            landmarks
        )

        shoulder_y = self.shoulder_y(
            landmarks
        )

        return wrist_y < shoulder_y

    # ========================================
    # WRIST HEIGHT DIFFERENCE
    # ========================================

    def wrist_shoulder_difference(
        self,
        landmarks
    ):

        return (
            self.shoulder_y(
                landmarks
            )
            -
            self.wrist_y(
                landmarks
            )
        )

    # ========================================
    # SHOULDER WIDTH
    # ========================================

    def shoulder_width(
        self,
        landmarks
    ):

        return self.distance(
            landmarks,
            11,
            12
        )

    # ========================================
    # HIP WIDTH
    # ========================================

    def hip_width(
        self,
        landmarks
    ):

        return self.distance(
            landmarks,
            23,
            24
        )

    # ========================================
    # LEFT ARM LENGTH
    # ========================================

    def left_arm_length(
        self,
        landmarks
    ):

        upper_arm = self.distance(
            landmarks,
            11,
            13
        )

        forearm = self.distance(
            landmarks,
            13,
            15
        )

        return (
            upper_arm +
            forearm
        )

    # ========================================
    # RIGHT ARM LENGTH
    # ========================================

    def right_arm_length(
        self,
        landmarks
    ):

        upper_arm = self.distance(
            landmarks,
            12,
            14
        )

        forearm = self.distance(
            landmarks,
            14,
            16
        )

        return (
            upper_arm +
            forearm
        )

    # ========================================
    # ARM SYMMETRY
    # ========================================

    def arm_symmetry(
        self,
        landmarks
    ):

        left = self.left_arm_length(
            landmarks
        )

        right = self.right_arm_length(
            landmarks
        )

        if left == 0 or right == 0:

            return 0.0

        difference = abs(
            left - right
        )

        average = (
            left +
            right
        ) / 2

        return max(
            0.0,
            1.0 -
            (
                difference /
                average
            )
        )

    # ========================================
    # KNEE SYMMETRY
    # ========================================

    def knee_symmetry(
        self,
        landmarks
    ):

        left = self.left_knee_angle(
            landmarks
        )

        right = self.right_knee_angle(
            landmarks
        )

        if left == 0 or right == 0:

            return 0.0

        difference = abs(
            left - right
        )

        return max(
            0.0,
            1.0 -
            (
                difference /
                180.0
            )
        )