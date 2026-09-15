
from workout.session import WorkoutSession


class WorkoutManager:

    def __init__(
        self,
        target_reps=10,
        target_sets=3,
        rest_seconds=30,
        weight_kg=70
    ):

        # ====================================
        # WORKOUT SESSION
        # ====================================

        self.session = WorkoutSession(

            target_reps=target_reps,

            target_sets=target_sets,

            rest_seconds=rest_seconds,

            weight_kg=weight_kg
        )

    # ========================================
    # START WORKOUT
    # ========================================

    def start(self):

        self.session.start_workout()

    # ========================================
    # ADD REP
    # ========================================

    def add_rep(
        self,
        form_score=0
    ):

        return (
            self.session.add_rep(
                form_score
            )
        )

    # ========================================
    # COMPLETE SET
    # ========================================

    def complete_set(self):

        return (
            self.session.complete_set()
        )

    # ========================================
    # UPDATE
    # ========================================

    def update(self):

        self.session.update_rest()

    # ========================================
    # RESET
    # ========================================

    def reset(self):

        self.session.reset()

    # ========================================
    # STATUS
    # ========================================

    def get_status(
        self,
        exercise="Unknown"
    ):

        return (
            self.session.get_status(
                exercise
            )
        )

    # ========================================
    # SUMMARY
    # ========================================

    def get_summary(
        self,
        exercise="Unknown"
    ):

        return (
            self.session.get_summary(
                exercise
            )
        )

    # ========================================
    # PROGRESS
    # ========================================

    def get_progress(self):

        return (
            self.session.get_progress()
        )

    # ========================================
    # REST
    # ========================================

    def get_remaining_rest(self):

        return (
            self.session
            .get_remaining_rest()
        )

    # ========================================
    # WORKOUT STATE
    # ========================================

    def is_active(self):

        return self.session.active

    def is_resting(self):

        return self.session.resting

    def is_complete(self):

        return (
            self.session.workout_complete
        )

