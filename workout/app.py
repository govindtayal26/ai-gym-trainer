
from workout.config import WorkoutConfig
from workout.live import LiveWorkout
from workout.ui import WorkoutUI
from workout.database import WorkoutDatabase


class WorkoutApp:

    def __init__(self):

        # ====================================
        # WORKOUT CONFIGURATION
        # ====================================

        self.config = WorkoutConfig()

        # ====================================
        # WORKOUT ENGINE
        # ====================================

        self.workout = LiveWorkout()

        # ====================================
        # USER INTERFACE
        # ====================================

        self.ui = WorkoutUI()

        # ====================================
        # DATABASE
        # ====================================

        self.database = WorkoutDatabase()

        # ====================================
        # CURRENT DATA
        # ====================================

        self.exercise = "Unknown"

        self.reps = 0

        self.form_score = 0

    # ========================================
    # CONFIGURE WORKOUT
    # ========================================

    def configure_workout(
        self,
        exercise,
        target_reps,
        target_sets,
        rest_seconds,
        weight_kg
    ):

        # ------------------------------------
        # Save configuration
        # ------------------------------------

        self.config.set_exercise(
            exercise
        )

        self.config.set_reps(
            target_reps
        )

        self.config.set_sets(
            target_sets
        )

        self.config.set_rest(
            rest_seconds
        )

        self.config.set_weight(
            weight_kg
        )

        # ------------------------------------
        # Configure live workout
        # ------------------------------------

        self.workout.configure(

            target_reps=self.config.target_reps,

            target_sets=self.config.target_sets,

            rest_seconds=self.config.rest_seconds,

            weight_kg=self.config.weight_kg
        )

        # ------------------------------------
        # Current exercise
        # ------------------------------------

        self.exercise = (
            self.config.exercise
        )

        self.reps = 0

        self.form_score = 0

    # ========================================
    # GET CONFIG
    # ========================================

    def get_config(self):

        return (
            self.config.get_config()
        )

    # ========================================
    # START WORKOUT
    # ========================================

    def start_workout(self):

        self.workout.start()

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

        return self.workout.update(

            exercise=exercise,

            reps=reps,

            form_score=form_score
        )

    # ========================================
    # COMPLETE SET
    # ========================================

    def complete_set(self):

        return (
            self.workout.complete_set()
        )

    # ========================================
    # RESET
    # ========================================

    def reset(self):

        self.workout.reset()

        self.exercise = "Unknown"

        self.reps = 0

        self.form_score = 0

    # ========================================
    # DRAW UI
    # ========================================

    def draw(
        self,
        frame
    ):

        status = (
            self.workout.get_status()
        )

        frame = (
            self.ui.draw_status(

                frame,

                status,

                self.exercise,

                self.form_score,

                self.reps
            )
        )

        frame = (
            self.ui.draw_controls(
                frame
            )
        )

        return frame

    # ========================================
    # GET STATUS
    # ========================================

    def get_status(self):

        return (
            self.workout.get_status()
        )

    # ========================================
    # GET SUMMARY
    # ========================================

    def get_summary(self):

        return (
            self.workout.get_summary()
        )

    # ========================================
    # SAVE WORKOUT
    # ========================================

    def save_workout(self):

        summary = (
            self.get_summary()
        )

        workout_id = (
            self.database.save_workout(

                exercise=self.exercise,

                total_sets=(
                    summary["total_sets"]
                ),

                total_reps=(
                    summary["total_reps"]
                ),

                average_form_score=(
                    summary[
                        "average_form_score"
                    ]
                ),

                duration_seconds=(
                    summary[
                        "duration_seconds"
                    ]
                ),

                calories_burned=(
                    summary[
                        "calories_burned"
                    ]
                ),

                completed=(
                    summary[
                        "completed"
                    ]
                )
            )
        )

        return workout_id

    # ========================================
    # GET WORKOUT HISTORY
    # ========================================

    def get_history(
        self,
        limit=10
    ):

        return (
            self.database
            .get_recent_workouts(
                limit
            )
        )

    # ========================================
    # GET TOTAL WORKOUTS
    # ========================================

    def get_total_workouts(self):

        return (
            self.database
            .get_total_workouts()
        )

    # ========================================
    # GET TOTAL REPS
    # ========================================

    def get_total_reps(self):

        return (
            self.database
            .get_total_reps()
        )

    # ========================================
    # GET TOTAL CALORIES
    # ========================================

    def get_total_calories(self):

        return (
            self.database
            .get_total_calories()
        )

    # ========================================
    # GET AVERAGE FORM
    # ========================================

    def get_average_form_score(self):

        return (
            self.database
            .get_average_form_score()
        )

    # ========================================
    # GET AVERAGE DURATION
    # ========================================

    def get_average_duration(self):

        return (
            self.database
            .get_average_duration()
        )

    # ========================================
    # GET EXERCISE STATISTICS
    # ========================================

    def get_exercise_statistics(
        self,
        exercise
    ):

        return (
            self.database
            .get_exercise_statistics(
                exercise
            )
        )

    # ========================================
    # DASHBOARD STATISTICS
    # ========================================

    def get_dashboard_statistics(self):

        return {

            "total_workouts":
                self.database
                .get_total_workouts(),

            "total_reps":
                self.database
                .get_total_reps(),

            "total_calories":
                self.database
                .get_total_calories(),

            "average_form":
                self.database
                .get_average_form_score(),

            "average_duration":
                self.database
                .get_average_duration()
        }

    # ========================================
    # DASHBOARD EXERCISES
    # ========================================

    def get_dashboard_exercises(self):

        exercises = [

            "Bicep Curl",

            "Squat",

            "Push-up"
        ]

        statistics = {}

        for exercise in exercises:

            statistics[exercise] = (

                self.database
                .get_exercise_statistics(
                    exercise
                )
            )

        return statistics

    # ========================================
    # DASHBOARD HISTORY
    # ========================================

    def get_dashboard_history(self):

        return (
            self.database
            .get_recent_workouts(
                limit=5
            )
        )

    # ========================================
    # CLOSE DATABASE
    # ========================================

    def close(self):

        self.database.close()

    # ========================================
    # WORKOUT ACTIVE
    # ========================================

    def is_active(self):

        return (
            self.workout.is_active()
        )

    # ========================================
    # WORKOUT RESTING
    # ========================================

    def is_resting(self):

        return (
            self.workout.is_resting()
        )

    # ========================================
    # WORKOUT COMPLETE
    # ========================================

    def is_complete(self):

        return (
            self.workout.engine
            .is_complete()
        )

