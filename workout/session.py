import time

from exercises.exercise_registry import ExerciseRegistry


class WorkoutSession:

    def __init__(
        self,
        target_reps=10,
        target_sets=3,
        rest_seconds=30,
        weight_kg=70
    ):

        # ========================================
        # EXERCISE REGISTRY
        # ========================================

        self.registry = ExerciseRegistry()

        # ========================================
        # WORKOUT SETTINGS
        # ========================================

        self.target_reps = target_reps
        self.target_sets = target_sets
        self.rest_seconds = rest_seconds
        self.weight_kg = weight_kg

        # ========================================
        # CURRENT PROGRESS
        # ========================================

        self.current_set = 1
        self.current_reps = 0

        self.total_sets = 0
        self.total_reps = 0

        # ========================================
        # FORM SCORES
        # ========================================

        self.form_scores = []

        # ========================================
        # STATE
        # ========================================

        self.active = False
        self.resting = False

        self.workout_complete = False

        # ========================================
        # REST
        # ========================================

        self.rest_start_time = None

        # ========================================
        # WORKOUT TIMER
        # ========================================

        self.start_time = None
        self.end_time = None

    # ========================================
    # START WORKOUT
    # ========================================

    def start_workout(self):

        self.active = True
        self.resting = False
        self.workout_complete = False

        self.current_set = 1
        self.current_reps = 0

        self.total_sets = 0
        self.total_reps = 0

        self.form_scores = []

        self.rest_start_time = None

        # ====================================
        # START TIMER
        # ====================================

        self.start_time = time.time()

        self.end_time = None

    # ========================================
    # ADD REP
    # ========================================

    def add_rep(
        self,
        form_score=0
    ):

        # ====================================
        # VALIDATION
        # ====================================

        if not self.active:
            return False

        if self.resting:
            return False

        if self.workout_complete:
            return False

        # ====================================
        # ADD REP
        # ====================================

        self.current_reps += 1

        self.total_reps += 1

        # ====================================
        # SAVE FORM SCORE
        # ====================================

        if form_score > 0:

            self.form_scores.append(
                form_score
            )

        # ====================================
        # PREVENT OVERFLOW
        # ====================================

        if (
            self.current_reps
            >
            self.target_reps
        ):

            self.current_reps = (
                self.target_reps
            )

        return True

    # ========================================
    # SET COMPLETE?
    # ========================================

    def is_set_complete(self):

        return (
            self.current_reps
            >=
            self.target_reps
        )

    # ========================================
    # COMPLETE SET
    # ========================================

    def complete_set(self):

        if not self.active:
            return False

        if self.resting:
            return False

        if self.current_reps <= 0:
            return False

        # ====================================
        # COMPLETE CURRENT SET
        # ====================================

        self.total_sets += 1

        # ====================================
        # LAST SET?
        # ====================================

        if (
            self.total_sets
            >=
            self.target_sets
        ):

            self.active = False

            self.resting = False

            self.workout_complete = True

            self.rest_start_time = None

            # =================================
            # STOP TIMER
            # =================================

            self.end_time = time.time()

            print(
                "\n"
                "================================"
            )

            print(
                "WORKOUT COMPLETE!"
            )

            print(
                "================================"
            )

            return True

        # ====================================
        # START NEXT SET
        # ====================================

        self.current_set += 1

        self.current_reps = 0

        self.start_rest()

        return True

    # ========================================
    # START REST
    # ========================================

    def start_rest(self):

        self.resting = True

        self.rest_start_time = (
            time.time()
        )

        print(
            "\n"
            f"REST STARTED: "
            f"{self.rest_seconds} seconds"
        )

    # ========================================
    # UPDATE REST
    # ========================================

    def update_rest(self):

        if not self.resting:
            return

        if self.rest_start_time is None:
            return

        elapsed = (
            time.time()
            -
            self.rest_start_time
        )

        if (
            elapsed
            >=
            self.rest_seconds
        ):

            self.resting = False

            self.rest_start_time = None

            print(
                "\n"
                "REST COMPLETE"
            )

    # ========================================
    # REMAINING REST
    # ========================================

    def get_remaining_rest(self):

        if not self.resting:
            return 0

        if self.rest_start_time is None:
            return self.rest_seconds

        elapsed = (
            time.time()
            -
            self.rest_start_time
        )

        remaining = (
            self.rest_seconds
            -
            elapsed
        )

        return max(
            0,
            int(
                round(
                    remaining
                )
            )
        )

    # ========================================
    # AVERAGE FORM SCORE
    # ========================================

    def average_form_score(self):

        if not self.form_scores:
            return 0

        return (
            sum(
                self.form_scores
            )
            /
            len(
                self.form_scores
            )
        )

    # ========================================
    # WORKOUT DURATION
    # ========================================

    def get_duration_seconds(self):

        if self.start_time is None:
            return 0

        if self.end_time is not None:

            return int(
                self.end_time
                -
                self.start_time
            )

        return int(
            time.time()
            -
            self.start_time
        )

    # ========================================
    # FORMATTED DURATION
    # ========================================

    def get_formatted_duration(self):

        total_seconds = (
            self.get_duration_seconds()
        )

        minutes = (
            total_seconds
            //
            60
        )

        seconds = (
            total_seconds
            %
            60
        )

        return (
            f"{minutes:02d}:{seconds:02d}"
        )

    # ========================================
    # MET VALUE
    # ========================================

    def get_met_value(
        self,
        exercise
    ):

        # ====================================
        # GET MET FROM REGISTRY
        # ====================================

        return (
            self.registry
            .get_met(
                exercise
            )
        )

    # ========================================
    # CALORIES
    # ========================================

    def get_calories_burned(
        self,
        exercise
    ):

        duration_minutes = (
            self.get_duration_seconds()
            /
            60
        )

        met = (
            self.get_met_value(
                exercise
            )
        )

        calories = (
            met
            *
            3.5
            *
            self.weight_kg
            /
            200
            *
            duration_minutes
        )

        return round(
            calories,
            2
        )

    # ========================================
    # PROGRESS
    # ========================================

    def get_progress(self):

        if self.target_reps <= 0:
            return 0

        progress = (
            self.current_reps
            /
            self.target_reps
        ) * 100

        return min(
            100,
            int(progress)
        )

    # ========================================
    # SUMMARY
    # ========================================

    def get_summary(
        self,
        exercise="Unknown"
    ):

        return {

            "exercise":
                exercise,

            "total_sets":
                self.total_sets,

            "target_sets":
                self.target_sets,

            "total_reps":
                self.total_reps,

            "target_reps":
                self.target_reps,

            "average_form_score":
                round(
                    self.average_form_score(),
                    1
                ),

            "duration_seconds":
                self.get_duration_seconds(),

            "duration":
                self.get_formatted_duration(),

            "calories_burned":
                self.get_calories_burned(
                    exercise
                ),

            "weight_kg":
                self.weight_kg,

            "completed":
                self.workout_complete
        }

    # ========================================
    # STATUS
    # ========================================

    def get_status(
        self,
        exercise="Unknown"
    ):

        # ====================================
        # UPDATE REST
        # ====================================

        self.update_rest()

        return {

            "set":
                self.current_set,

            "set_reps":
                self.current_reps,

            "reps":
                self.current_reps,

            "total_sets":
                self.total_sets,

            "total_reps":
                self.total_reps,

            "target_sets":
                self.target_sets,

            "target_reps":
                self.target_reps,

            "form_score":
                round(
                    self.average_form_score(),
                    1
                ),

            "active":
                self.active,

            "resting":
                self.resting,

            "rest_remaining":
                self.get_remaining_rest(),

            "workout_complete":
                self.workout_complete,

            "complete":
                self.workout_complete,

            "duration_seconds":
                self.get_duration_seconds(),

            "duration":
                self.get_formatted_duration(),

            "calories_burned":
                self.get_calories_burned(
                    exercise
                ),

            "weight_kg":
                self.weight_kg,

            "progress":
                self.get_progress()
        }

    # ========================================
    # GET EXERCISE INFO
    # ========================================

    def get_exercise_info(
        self,
        exercise
    ):

        return (
            self.registry
            .get_info(
                exercise
            )
        )

    # ========================================
    # GET EXERCISE MET
    # ========================================

    def get_exercise_met(
        self,
        exercise
    ):

        return (
            self.registry
            .get_met(
                exercise
            )
        )

    # ========================================
    # RESET
    # ========================================

    def reset(self):

        self.current_set = 1

        self.current_reps = 0

        self.total_sets = 0

        self.total_reps = 0

        self.form_scores = []

        self.active = False

        self.resting = False

        self.workout_complete = False

        self.rest_start_time = None

        self.start_time = None

        self.end_time = None