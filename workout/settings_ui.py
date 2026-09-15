import cv2

from exercises.exercise_registry import ExerciseRegistry


class SettingsUI:

    def __init__(self):

        # ========================================
        # EXERCISE REGISTRY
        # ========================================

        self.registry = ExerciseRegistry()

        self.exercises = (
            self.registry.get_exercises()
        )

        self.exercise_index = 0

        # ========================================
        # WORKOUT SETTINGS
        # ========================================

        self.target_reps = 10
        self.target_sets = 3
        self.rest_seconds = 30
        self.weight_kg = 70

        # ========================================
        # SELECTED OPTION
        # ========================================

        self.selected = 0

        self.options = [
            "exercise",
            "reps",
            "sets",
            "rest",
            "weight"
        ]

    # ========================================
    # REFRESH EXERCISES
    # ========================================

    def refresh_exercises(self):

        self.exercises = (
            self.registry.get_exercises()
        )

        # Protect against an invalid
        # exercise index.

        if not self.exercises:

            self.exercise_index = 0

            return

        if (
            self.exercise_index
            >=
            len(self.exercises)
        ):

            self.exercise_index = 0

    # ========================================
    # EXERCISE
    # ========================================

    def next_exercise(self):

        self.refresh_exercises()

        if not self.exercises:
            return

        self.exercise_index += 1

        if (
            self.exercise_index
            >=
            len(self.exercises)
        ):

            self.exercise_index = 0

    def previous_exercise(self):

        self.refresh_exercises()

        if not self.exercises:
            return

        self.exercise_index -= 1

        if self.exercise_index < 0:

            self.exercise_index = (
                len(self.exercises) - 1
            )

    # ========================================
    # REPS
    # ========================================

    def increase_reps(self):

        self.target_reps += 1

        if self.target_reps > 100:

            self.target_reps = 100

    def decrease_reps(self):

        self.target_reps -= 1

        if self.target_reps < 1:

            self.target_reps = 1

    # ========================================
    # SETS
    # ========================================

    def increase_sets(self):

        self.target_sets += 1

        if self.target_sets > 20:

            self.target_sets = 20

    def decrease_sets(self):

        self.target_sets -= 1

        if self.target_sets < 1:

            self.target_sets = 1

    # ========================================
    # REST
    # ========================================

    def increase_rest(self):

        self.rest_seconds += 5

        if self.rest_seconds > 300:

            self.rest_seconds = 300

    def decrease_rest(self):

        self.rest_seconds -= 5

        if self.rest_seconds < 0:

            self.rest_seconds = 0

    # ========================================
    # WEIGHT
    # ========================================

    def increase_weight(self):

        self.weight_kg += 1

        if self.weight_kg > 300:

            self.weight_kg = 300

    def decrease_weight(self):

        self.weight_kg -= 1

        if self.weight_kg < 1:

            self.weight_kg = 1

    # ========================================
    # NAVIGATION
    # ========================================

    def select_next(self):

        self.selected += 1

        if (
            self.selected
            >=
            len(self.options)
        ):

            self.selected = 0

    def select_previous(self):

        self.selected -= 1

        if self.selected < 0:

            self.selected = (
                len(self.options) - 1
            )

    # ========================================
    # CURRENT EXERCISE
    # ========================================

    def get_exercise(self):

        self.refresh_exercises()

        if not self.exercises:

            return "Unknown"

        return self.exercises[
            self.exercise_index
        ]

    # ========================================
    # CONFIG
    # ========================================

    def get_config(self):

        return {

            "exercise":
                self.get_exercise(),

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
    # DRAW SETTINGS SCREEN
    # ========================================

    def draw(self, frame):

        height, width = (
            frame.shape[:2]
        )

        # ====================================
        # REFRESH EXERCISES
        # ====================================

        self.refresh_exercises()

        # ====================================
        # DARK OVERLAY
        # ====================================

        overlay = frame.copy()

        cv2.rectangle(

            overlay,

            (0, 0),

            (width, height),

            (20, 20, 20),

            -1
        )

        frame = cv2.addWeighted(

            overlay,

            0.85,

            frame,

            0.15,

            0
        )

        # ====================================
        # TITLE
        # ====================================

        cv2.putText(

            frame,

            "AI GYM TRAINER",

            (
                width // 2 - 220,
                70
            ),

            cv2.FONT_HERSHEY_SIMPLEX,

            1.5,

            (0, 255, 255),

            3
        )

        cv2.putText(

            frame,

            "WORKOUT SETTINGS",

            (
                width // 2 - 190,
                115
            ),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.9,

            (255, 255, 255),

            2
        )

        # ====================================
        # SETTINGS
        # ====================================

        settings = [

            (
                "Exercise",
                self.get_exercise()
            ),

            (
                "Target Reps",
                str(self.target_reps)
            ),

            (
                "Target Sets",
                str(self.target_sets)
            ),

            (
                "Rest",
                f"{self.rest_seconds} sec"
            ),

            (
                "Weight",
                f"{self.weight_kg} kg"
            )
        ]

        start_y = 180

        for index, (
            label,
            value
        ) in enumerate(settings):

            y = (
                start_y
                +
                index * 70
            )

            # =================================
            # SELECTED ROW
            # =================================

            if index == self.selected:

                cv2.rectangle(

                    frame,

                    (
                        width // 2 - 300,
                        y - 35
                    ),

                    (
                        width // 2 + 300,
                        y + 20
                    ),

                    (50, 50, 50),

                    -1
                )

                text_color = (
                    0,
                    255,
                    255
                )

            else:

                text_color = (
                    255,
                    255,
                    255
                )

            # =================================
            # LABEL
            # =================================

            cv2.putText(

                frame,

                label,

                (
                    width // 2 - 270,
                    y
                ),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.7,

                text_color,

                2
            )

            # =================================
            # VALUE
            # =================================

            cv2.putText(

                frame,

                value,

                (
                    width // 2 + 50,
                    y
                ),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.7,

                (255, 255, 255),

                2
            )

        # ====================================
        # CONTROLS
        # ====================================

        controls_y = (
            height - 130
        )

        cv2.putText(

            frame,

            "UP/DOWN : Select",

            (
                40,
                controls_y
            ),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.55,

            (220, 220, 220),

            1
        )

        cv2.putText(

            frame,

            "LEFT/RIGHT : Change",

            (
                40,
                controls_y + 30
            ),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.55,

            (220, 220, 220),

            1
        )

        cv2.putText(

            frame,

            "ENTER : Start Workout",

            (
                40,
                controls_y + 60
            ),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.55,

            (0, 255, 0),

            2
        )

        cv2.putText(

            frame,

            "Q : Quit",

            (
                40,
                controls_y + 90
            ),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.55,

            (220, 220, 220),

            1
        )

        # ====================================
        # EXERCISE INFORMATION
        # ====================================

        exercise_name = (
            self.get_exercise()
        )

        info = (
            self.registry
            .get_info(
                exercise_name
            )
        )

        if info is not None:

            muscles = ", ".join(
                info["muscles"]
            )

            info_text = (
                f"Muscles: {muscles}"
            )

            cv2.putText(

                frame,

                info_text,

                (
                    width // 2 - 300,
                    height - 55
                ),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.5,

                (180, 180, 180),

                1
            )

        return frame

    # ========================================
    # HANDLE KEY
    # ========================================

    def handle_key(self, key):

        # ====================================
        # UP
        # ====================================

        if key == 2490368:

            self.select_previous()

        # ====================================
        # DOWN
        # ====================================

        elif key == 2621440:

            self.select_next()

        # ====================================
        # LEFT
        # ====================================

        elif key == 2424832:

            self.decrease_selected()

        # ====================================
        # RIGHT
        # ====================================

        elif key == 2555904:

            self.increase_selected()

    # ========================================
    # INCREASE SELECTED
    # ========================================

    def increase_selected(self):

        option = self.options[
            self.selected
        ]

        if option == "exercise":

            self.next_exercise()

        elif option == "reps":

            self.increase_reps()

        elif option == "sets":

            self.increase_sets()

        elif option == "rest":

            self.increase_rest()

        elif option == "weight":

            self.increase_weight()

    # ========================================
    # DECREASE SELECTED
    # ========================================

    def decrease_selected(self):

        option = self.options[
            self.selected
        ]

        if option == "exercise":

            self.previous_exercise()

        elif option == "reps":

            self.decrease_reps()

        elif option == "sets":

            self.decrease_sets()

        elif option == "rest":

            self.decrease_rest()

        elif option == "weight":

            self.decrease_weight()

    # ========================================
    # RESET
    # ========================================

    def reset(self):

        self.refresh_exercises()

        self.exercise_index = 0

        self.target_reps = 10

        self.target_sets = 3

        self.rest_seconds = 30

        self.weight_kg = 70

        self.selected = 0