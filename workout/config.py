
class WorkoutConfig:

    def __init__(
        self,
        exercise="Bicep Curl",
        target_reps=10,
        target_sets=3,
        rest_seconds=30,
        weight_kg=70
    ):

        # ====================================
        # EXERCISE
        # ====================================

        self.exercise = exercise

        # ====================================
        # WORKOUT TARGET
        # ====================================

        self.target_reps = target_reps

        self.target_sets = target_sets

        # ====================================
        # REST
        # ====================================

        self.rest_seconds = rest_seconds

        # ====================================
        # USER WEIGHT
        # ====================================

        self.weight_kg = weight_kg

    # ========================================
    # SET EXERCISE
    # ========================================

    def set_exercise(
        self,
        exercise
    ):

        self.exercise = exercise

    # ========================================
    # SET REPS
    # ========================================

    def set_reps(
        self,
        reps
    ):

        reps = int(reps)

        if reps < 1:
            reps = 1

        self.target_reps = reps

    # ========================================
    # SET SETS
    # ========================================

    def set_sets(
        self,
        sets
    ):

        sets = int(sets)

        if sets < 1:
            sets = 1

        self.target_sets = sets

    # ========================================
    # SET REST
    # ========================================

    def set_rest(
        self,
        seconds
    ):

        seconds = int(seconds)

        if seconds < 0:
            seconds = 0

        self.rest_seconds = seconds

    # ========================================
    # SET WEIGHT
    # ========================================

    def set_weight(
        self,
        weight
    ):

        weight = float(weight)

        if weight <= 0:
            weight = 1

        self.weight_kg = weight

    # ========================================
    # GET CONFIG
    # ========================================

    def get_config(self):

        return {

            "exercise":
                self.exercise,

            "target_reps":
                self.target_reps,

            "target_sets":
                self.target_sets,

            "rest_seconds":
                self.rest_seconds,

            "weight_kg":
                self.weight_kg
        }

    # ========================================
    # RESET DEFAULTS
    # ========================================

    def reset(self):

        self.exercise = "Bicep Curl"

        self.target_reps = 10

        self.target_sets = 3

        self.rest_seconds = 30

        self.weight_kg = 70

