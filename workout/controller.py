
from workout.manager import WorkoutManager


class WorkoutController:

    def __init__(
        self,
        target_reps=10,
        target_sets=3,
        rest_seconds=30,
        weight_kg=70
    ):

        self.manager = WorkoutManager(

            target_reps=target_reps,

            target_sets=target_sets,

            rest_seconds=rest_seconds,

            weight_kg=weight_kg
        )

    # ========================================
    # START WORKOUT
    # ========================================

    def start_workout(self):

        self.manager.start()

    # ========================================
    # ADD REP
    # ========================================

    def add_rep(
        self,
        form_score=0
    ):

        return self.manager.add_rep(
            form_score
        )

    # ========================================
    # COMPLETE SET
    # ========================================

    def complete_set(self):

        return self.manager.complete_set()

    # ========================================
    # UPDATE
    # ========================================

    def update(self):

        self.manager.update()

    # ========================================
    # RESET
    # ========================================

    def reset_workout(self):

        self.manager.reset()

    # ========================================
    # STATUS
    # ========================================

    def get_status(
        self,
        exercise="Unknown"
    ):

        return self.manager.get_status(
            exercise
        )

    # ========================================
    # SUMMARY
    # ========================================

    def get_summary(
        self,
        exercise="Unknown"
    ):

        return self.manager.get_summary(
            exercise
        )

    # ========================================
    # PROGRESS
    # ========================================

    def get_progress(self):

        return self.manager.get_progress()

    # ========================================
    # REST
    # ========================================

    def get_remaining_rest(self):

        return self.manager.get_remaining_rest()

    # ========================================
    # STATE
    # ========================================

    def is_resting(self):

        return self.manager.is_resting()

    def is_workout_active(self):

        return self.manager.is_active()

    def is_workout_complete(self):

        return self.manager.is_complete()
