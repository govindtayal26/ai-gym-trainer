
from workout.controller import WorkoutController


class WorkoutEngine:

    def __init__(self):

        # ====================================
        # WORKOUT CONTROLLER
        # ====================================

        self.controller = WorkoutController()

        # ====================================
        # CURRENT WORKOUT
        # ====================================

        self.exercise = "Unknown"

        self.form_score = 0

        # ====================================
        # REP TRACKING
        # ====================================

        self.previous_reps = 0

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

        self.controller = WorkoutController(

            target_reps=target_reps,

            target_sets=target_sets,

            rest_seconds=rest_seconds,

            weight_kg=weight_kg
        )

        self.exercise = "Unknown"

        self.form_score = 0

        self.previous_reps = 0

    # ========================================
    # START
    # ========================================

    def start(self):

        self.controller.start_workout()

        self.previous_reps = 0

        print(
            "Workout engine started"
        )

    # ========================================
    # UPDATE
    # ========================================

    def update(
        self,
        exercise,
        current_reps,
        form_score
    ):

        # ------------------------------------
        # Update exercise
        # ------------------------------------

        self.exercise = exercise

        self.form_score = form_score

        # ------------------------------------
        # Update rest timer
        # ------------------------------------

        self.controller.update()

        # ------------------------------------
        # Unknown exercise
        # ------------------------------------

        if exercise == "Unknown":

            return self.get_status()

        # ------------------------------------
        # Workout not active
        # ------------------------------------

        if not self.controller.is_workout_active():

            return self.get_status()

        # ------------------------------------
        # Currently resting
        # ------------------------------------

        if self.controller.is_resting():

            self.previous_reps = current_reps

            return self.get_status()

        # ------------------------------------
        # Detect new reps
        # ------------------------------------

        if current_reps > self.previous_reps:

            difference = (
                current_reps
                -
                self.previous_reps
            )

            # --------------------------------
            # Add newly detected reps
            # --------------------------------

            for _ in range(difference):

                self.controller.add_rep(
                    form_score
                )

        # ------------------------------------
        # Update previous reps
        # ------------------------------------

        self.previous_reps = current_reps

        # ------------------------------------
        # Get status
        # ------------------------------------

        status = (
            self.controller
            .get_status(
                self.exercise
            )
        )

        # ------------------------------------
        # Automatic set completion
        # ------------------------------------

        if (
            status["set_reps"]
            >=
            status["target_reps"]
        ):

            self.controller.complete_set()

            self.previous_reps = 0

        return self.get_status()

    # ========================================
    # COMPLETE SET
    # ========================================

    def complete_set(self):

        result = (
            self.controller
            .complete_set()
        )

        self.previous_reps = 0

        return result

    # ========================================
    # RESET
    # ========================================

    def reset(self):

        self.controller.reset()

        self.previous_reps = 0

        self.exercise = "Unknown"

        self.form_score = 0

    # ========================================
    # STATUS
    # ========================================

    def get_status(self):

        return (
            self.controller
            .get_status(
                self.exercise
            )
        )

    # ========================================
    # SUMMARY
    # ========================================

    def get_summary(self):

        return (
            self.controller
            .get_summary(
                self.exercise
            )
        )

    # ========================================
    # PROGRESS
    # ========================================

    def get_progress(self):

        return (
            self.controller
            .get_progress()
        )

    # ========================================
    # ACTIVE
    # ========================================

    def is_active(self):

        return (
            self.controller
            .is_workout_active()
        )

    # ========================================
    # RESTING
    # ========================================

    def is_resting(self):

        return (
            self.controller
            .is_resting()
        )

    # ========================================
    # REST REMAINING
    # ========================================

    def get_remaining_rest(self):

        return (
            self.controller
            .get_remaining_rest()
        )

    # ========================================
    # COMPLETE
    # ========================================

    def is_complete(self):

        return (
            self.controller
            .is_workout_complete()
        )
