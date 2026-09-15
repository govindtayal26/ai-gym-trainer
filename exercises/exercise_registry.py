from exercises.bicep_curl import BicepCurl
from exercises.squat import Squat
from exercises.pushup import PushUp
from exercises.shoulder_press import ShoulderPress
from exercises.lateral_raise import LateralRaise


class ExerciseRegistry:

    def __init__(self):

        # ========================================
        # EXERCISE DEFINITIONS
        # ========================================

        self.exercises = {

            # ====================================
            # BICEP CURL
            # ====================================

            "Bicep Curl": {

                "class": BicepCurl,

                "category": "Arms",

                "muscles": [
                    "Biceps"
                ],

                "difficulty": "Beginner",

                "met": 3.5,

                "recognition": {

                    "primary_joints": [
                        "shoulder",
                        "elbow",
                        "wrist"
                    ],

                    "movement": "elbow_flexion",

                    "orientation": "standing"
                },

                "form": {

                    "primary_angle": "elbow",

                    "target_range": (
                        50,
                        160
                    ),

                    "symmetry_required": False
                },

                "coaching": {

                    "focus": [
                        "elbow_stability",
                        "full_range",
                        "controlled_movement"
                    ]
                }
            },

            # ====================================
            # SQUAT
            # ====================================

            "Squat": {

                "class": Squat,

                "category": "Legs",

                "muscles": [
                    "Quadriceps",
                    "Glutes",
                    "Hamstrings"
                ],

                "difficulty": "Beginner",

                "met": 5.0,

                "recognition": {

                    "primary_joints": [
                        "hip",
                        "knee",
                        "ankle"
                    ],

                    "movement": "knee_flexion",

                    "orientation": "standing"
                },

                "form": {

                    "primary_angle": "knee",

                    "target_range": (
                        70,
                        165
                    ),

                    "symmetry_required": True
                },

                "coaching": {

                    "focus": [
                        "depth",
                        "knee_alignment",
                        "torso_position"
                    ]
                }
            },

            # ====================================
            # PUSH-UP
            # ====================================

            "Push-up": {

                "class": PushUp,

                "category": "Chest",

                "muscles": [
                    "Chest",
                    "Triceps",
                    "Shoulders"
                ],

                "difficulty": "Beginner",

                "met": 6.0,

                "recognition": {

                    "primary_joints": [
                        "shoulder",
                        "elbow",
                        "wrist",
                        "hip"
                    ],

                    "movement": "horizontal_press",

                    "orientation": "horizontal"
                },

                "form": {

                    "primary_angle": "elbow",

                    "target_range": (
                        80,
                        160
                    ),

                    "symmetry_required": True
                },

                "coaching": {

                    "focus": [
                        "body_alignment",
                        "depth",
                        "elbow_position"
                    ]
                }
            },

            # ====================================
            # SHOULDER PRESS
            # ====================================

            "Shoulder Press": {

                "class": ShoulderPress,

                "category": "Shoulders",

                "muscles": [
                    "Shoulders",
                    "Triceps"
                ],

                "difficulty": "Intermediate",

                "met": 5.0,

                "recognition": {

                    "primary_joints": [
                        "shoulder",
                        "elbow",
                        "wrist"
                    ],

                    "movement": "vertical_press",

                    "orientation": "standing"
                },

                "form": {

                    "primary_angle": "elbow",

                    "target_range": (
                        90,
                        170
                    ),

                    "symmetry_required": True
                },

                "coaching": {

                    "focus": [
                        "press_height",
                        "elbow_control",
                        "torso_position"
                    ]
                }
            },

            # ====================================
            # LATERAL RAISE
            # ====================================

            "Lateral Raise": {

                "class": LateralRaise,

                "category": "Shoulders",

                "muscles": [
                    "Side Delts"
                ],

                "difficulty": "Beginner",

                "met": 3.5,

                "recognition": {

                    "primary_joints": [
                        "shoulder",
                        "elbow",
                        "wrist"
                    ],

                    "movement": "shoulder_abduction",

                    "orientation": "standing"
                },

                "form": {

                    "primary_angle": "shoulder",

                    "target_range": (
                        20,
                        90
                    ),

                    "symmetry_required": True
                },

                "coaching": {

                    "focus": [
                        "arm_height",
                        "symmetry",
                        "elbow_position"
                    ]
                }
            }
        }

    # ========================================
    # GET ALL EXERCISES
    # ========================================

    def get_exercises(self):

        return list(
            self.exercises.keys()
        )

    # ========================================
    # GET DEFINITION
    # ========================================

    def get_definition(
        self,
        exercise_name
    ):

        return self.exercises.get(
            exercise_name
        )

    # ========================================
    # GET CLASS
    # ========================================

    def get_class(
        self,
        exercise_name
    ):

        definition = (
            self.get_definition(
                exercise_name
            )
        )

        if definition is None:
            return None

        return definition["class"]

    # ========================================
    # CREATE EXERCISE
    # ========================================

    def create(
        self,
        exercise_name
    ):

        exercise_class = (
            self.get_class(
                exercise_name
            )
        )

        if exercise_class is None:
            return None

        return exercise_class()

    # ========================================
    # CHECK EXISTENCE
    # ========================================

    def has_exercise(
        self,
        exercise_name
    ):

        return (
            exercise_name
            in
            self.exercises
        )

    # ========================================
    # CATEGORY
    # ========================================

    def get_category(
        self,
        exercise_name
    ):

        definition = (
            self.get_definition(
                exercise_name
            )
        )

        if definition is None:
            return None

        return definition["category"]

    # ========================================
    # MUSCLES
    # ========================================

    def get_muscles(
        self,
        exercise_name
    ):

        definition = (
            self.get_definition(
                exercise_name
            )
        )

        if definition is None:
            return []

        return definition["muscles"]

    # ========================================
    # DIFFICULTY
    # ========================================

    def get_difficulty(
        self,
        exercise_name
    ):

        definition = (
            self.get_definition(
                exercise_name
            )
        )

        if definition is None:
            return None

        return definition["difficulty"]

    # ========================================
    # MET
    # ========================================

    def get_met(
        self,
        exercise_name
    ):

        definition = (
            self.get_definition(
                exercise_name
            )
        )

        if definition is None:
            return 4.0

        return definition["met"]

    # ========================================
    # RECOGNITION PROFILE
    # ========================================

    def get_recognition_profile(
        self,
        exercise_name
    ):

        definition = (
            self.get_definition(
                exercise_name
            )
        )

        if definition is None:
            return None

        return definition["recognition"]

    # ========================================
    # FORM PROFILE
    # ========================================

    def get_form_profile(
        self,
        exercise_name
    ):

        definition = (
            self.get_definition(
                exercise_name
            )
        )

        if definition is None:
            return None

        return definition["form"]

    # ========================================
    # COACHING PROFILE
    # ========================================

    def get_coaching_profile(
        self,
        exercise_name
    ):

        definition = (
            self.get_definition(
                exercise_name
            )
        )

        if definition is None:
            return None

        return definition["coaching"]

    # ========================================
    # COMPLETE INFORMATION
    # ========================================

    def get_info(
        self,
        exercise_name
    ):

        definition = (
            self.get_definition(
                exercise_name
            )
        )

        if definition is None:
            return None

        return {

            "name":
                exercise_name,

            "category":
                definition["category"],

            "muscles":
                definition["muscles"],

            "difficulty":
                definition["difficulty"],

            "met":
                definition["met"],

            "recognition":
                definition["recognition"],

            "form":
                definition["form"],

            "coaching":
                definition["coaching"]
        }