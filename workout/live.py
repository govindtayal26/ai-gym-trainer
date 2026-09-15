
from workout.engine import WorkoutEngine


class LiveWorkout:

    def __init__(self):

        # ====================================
        # WORKOUT ENGINE
        # ====================================

        self.engine = WorkoutEngine()

        # ====================================
        # CURRENT WORKOUT DATA
        # ====================================

        self.exercise = "Unknown"

        self.reps = 0

        self.form_score = 0

    # ========================================
    # CONFIGURE WORKOUT
    # ========================================

    def configure(
        self,
        target_reps,
        target_sets,
        rest_seconds,
        weight_kg
    ):

        self.engine.configure(

            target_reps=target_reps,

            target_sets=target_sets,

            rest_seconds=rest_seconds,

            weight_kg=weight_kg
        )

        # Reset live data

        self.reps = 0

        self.form_score = 0

    # ========================================
    # START WORKOUT
    # ========================================

    def start(self):

        self.engine.start()

    # ========================================
    # UPDATE WORKOUT
    # ========================================

    def update(
        self,
        exercise,
        reps,
        form_score
    ):

        self.exercise = exercise

        self.reps = reps

        self.form_score = form_score

        return self.engine.update(

            exercise=exercise,

            current_reps=reps,

            form_score=form_score
        )

    # ========================================
    # COMPLETE SET
    # ========================================

    def complete_set(self):

        return (
            self.engine.complete_set()
        )

    # ========================================
    # RESET
    # ========================================

    def reset(self):

        self.engine.reset()

        self.exercise = "Unknown"

        self.reps = 0

        self.form_score = 0

    # ========================================
    # GET STATUS
    # ========================================

    def get_status(self):

        return (
            self.engine.get_status()
        )

    # ========================================
    # GET SUMMARY
    # ========================================

    def get_summary(self):

        return (
            self.engine.get_summary()
        )

    # ========================================
    # ACTIVE
    # ========================================

    def is_active(self):

        return (
            self.engine.is_active()
        )

    # ========================================
    # RESTING
    # ========================================

    def is_resting(self):

        return (
            self.engine.is_resting()
        )

    # ========================================
    # COMPLETE
    # ========================================

    def is_complete(self):

        return (
            self.engine.is_complete()
        )

    # ========================================
    # REMAINING REST
    # ========================================

    def get_remaining_rest(self):

        return (
            self.engine.get_remaining_rest()
        )
