from exercises.exercise_registry import ExerciseRegistry


class ExerciseManager:

    def __init__(self):

        # ========================================
        # REGISTRY
        # ========================================

        self.registry = (
            ExerciseRegistry()
        )

        # ========================================
        # CREATE EXERCISES
        # ========================================

        self.exercises = {}

        for exercise_name in (
            self.registry.get_exercises()
        ):

            exercise = (
                self.registry.create(
                    exercise_name
                )
            )

            if exercise is not None:

                self.exercises[
                    exercise_name
                ] = exercise

        # ========================================
        # CURRENT EXERCISE
        # ========================================

        self.current_exercise = None

    # ========================================
    # SET EXERCISE
    # ========================================

    def set_exercise(
        self,
        exercise_name
    ):

        if (
            exercise_name
            not in
            self.exercises
        ):

            self.current_exercise = None

            return False

        # ====================================
        # ONLY RESET WHEN CHANGED
        # ====================================

        if (
            self.current_exercise
            !=
            exercise_name
        ):

            self.current_exercise = (
                exercise_name
            )

            self.exercises[
                exercise_name
            ].reset()

        return True

    # ========================================
    # UPDATE
    # ========================================

    def update(
        self,
        landmarks
    ):

        # ====================================
        # NO EXERCISE
        # ====================================

        if (
            self.current_exercise
            is None
        ):

            return {

                "exercise":
                    "Unknown",

                "reps":
                    0,

                "stage":
                    "unknown",

                "form_score":
                    0,

                "feedback":
                    "Select an exercise"
            }

        # ====================================
        # CURRENT EXERCISE
        # ====================================

        exercise = (
            self.exercises[
                self.current_exercise
            ]
        )

        result = (
            exercise.update(
                landmarks
            )
        )

        # ====================================
        # ADD NAME
        # ====================================

        result["exercise"] = (
            self.current_exercise
        )

        return result

    # ========================================
    # CURRENT EXERCISE
    # ========================================

    def get_current_exercise(self):

        return self.current_exercise

    # ========================================
    # RESET
    # ========================================

    def reset(self):

        if (
            self.current_exercise
            is not None
        ):

            exercise = (
                self.exercises[
                    self.current_exercise
                ]
            )

            exercise.reset()

    # ========================================
    # AVAILABLE EXERCISES
    # ========================================

    def get_available_exercises(self):

        return (
            self.registry
            .get_exercises()
        )

    # ========================================
    # GET EXERCISE
    # ========================================

    def get_exercise(
        self,
        exercise_name
    ):

        return self.exercises.get(
            exercise_name
        )

    # ========================================
    # HAS EXERCISE
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
    # EXERCISE INFO
    # ========================================

    def get_exercise_info(
        self,
        exercise_name
    ):

        return (
            self.registry
            .get_info(
                exercise_name
            )
        )

    # ========================================
    # EXERCISE CATEGORY
    # ========================================

    def get_category(
        self,
        exercise_name
    ):

        return (
            self.registry
            .get_category(
                exercise_name
            )
        )

    # ========================================
    # EXERCISE MUSCLES
    # ========================================

    def get_muscles(
        self,
        exercise_name
    ):

        return (
            self.registry
            .get_muscles(
                exercise_name
            )
        )

    # ========================================
    # EXERCISE DIFFICULTY
    # ========================================

    def get_difficulty(
        self,
        exercise_name
    ):

        return (
            self.registry
            .get_difficulty(
                exercise_name
            )
        )

    # ========================================
    # EXERCISE MET
    # ========================================

    def get_met(
        self,
        exercise_name
    ):

        return (
            self.registry
            .get_met(
                exercise_name
            )
        )