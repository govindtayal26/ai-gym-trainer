
import cv2


class WorkoutUI:

    def __init__(self):

        self.font = cv2.FONT_HERSHEY_SIMPLEX

    # ====================================
    # TEXT
    # ====================================

    def draw_text(
        self,
        frame,
        text,
        position,
        size=0.7,
        thickness=2
    ):

        cv2.putText(
            frame,
            text,
            position,
            self.font,
            size,
            (255, 255, 255),
            thickness,
            cv2.LINE_AA
        )

    # ====================================
    # PROGRESS BAR
    # ====================================

    def draw_progress_bar(
        self,
        frame,
        current,
        target,
        x,
        y,
        width=350,
        height=25
    ):

        if target <= 0:

            progress = 0

        else:

            progress = min(
                current / target,
                1.0
            )

        filled_width = int(
            width * progress
        )

        # --------------------------------
        # Border
        # --------------------------------

        cv2.rectangle(
            frame,
            (x, y),
            (x + width, y + height),
            (100, 100, 100),
            2
        )

        # --------------------------------
        # Filled progress
        # --------------------------------

        if filled_width > 0:

            cv2.rectangle(
                frame,
                (x, y),
                (
                    x + filled_width,
                    y + height
                ),
                (0, 255, 0),
                -1
            )

    # ====================================
    # STATUS LABEL
    # ====================================

    def get_workout_state(
        self,
        status
    ):

        if status.get(
            "workout_complete",
            False
        ):

            return "COMPLETE"

        if status.get(
            "resting",
            False
        ):

            return "REST"

        if status.get(
            "active",
            False
        ):

            return "ACTIVE"

        return "READY"

    # ====================================
    # STATUS
    # ====================================

    def draw_status(
        self,
        frame,
        status,
        exercise,
        form_score,
        exercise_reps=0
    ):

        height, width = (
            frame.shape[:2]
        )

        # =================================
        # GET STATUS VALUES
        # =================================

        current_set = status.get(
            "set",
            1
        )

        target_sets = status.get(
            "target_sets",
            3
        )

        target_reps = status.get(
            "target_reps",
            10
        )

        total_reps = status.get(
            "total_reps",
            0
        )

        resting = status.get(
            "resting",
            False
        )

        active = status.get(
            "active",
            False
        )

        workout_complete = status.get(
            "workout_complete",
            False
        )

        remaining = status.get(
            "rest_remaining",
            0
        )

        # =================================
        # WORKOUT STATE
        # =================================

        workout_state = (
            self.get_workout_state(
                status
            )
        )

        # =================================
        # HEADER
        # =================================

        self.draw_text(
            frame,
            "AI GYM TRAINER",
            (20, 40),
            size=1.0,
            thickness=2
        )

        # =================================
        # WORKOUT STATE
        # =================================

        self.draw_text(
            frame,
            f"STATUS: {workout_state}",
            (20, 70),
            size=0.65
        )

        # =================================
        # EXERCISE
        # =================================

        self.draw_text(
            frame,
            f"Exercise: {exercise}",
            (20, 105),
            size=0.75
        )

        # =================================
        # SET
        # =================================

        self.draw_text(
            frame,
            f"SET: {current_set} / {target_sets}",
            (20, 145),
            size=0.75
        )

        # =================================
        # REPS
        # =================================

        self.draw_text(
            frame,
            f"REPS: {exercise_reps} / {target_reps}",
            (20, 185),
            size=0.75
        )

        # =================================
        # TOTAL REPS
        # =================================

        self.draw_text(
            frame,
            f"TOTAL REPS: {total_reps}",
            (20, 225),
            size=0.7
        )

        # =================================
        # FORM SCORE
        # =================================

        self.draw_text(
            frame,
            f"FORM SCORE: {form_score}",
            (20, 265),
            size=0.75
        )

        # =================================
        # PROGRESS
        # =================================

        self.draw_progress_bar(
            frame,
            exercise_reps,
            target_reps,
            20,
            290
        )

        # =================================
        # REST SCREEN
        # =================================

        if resting:

            overlay = frame.copy()

            cv2.rectangle(
                overlay,
                (0, 0),
                (width, height),
                (0, 0, 0),
                -1
            )

            frame = cv2.addWeighted(
                overlay,
                0.70,
                frame,
                0.30,
                0
            )

            # --------------------------------
            # SET COMPLETE
            # --------------------------------

            self.draw_text(
                frame,
                "SET COMPLETE",
                (
                    width // 2 - 150,
                    height // 2 - 100
                ),
                size=1.0,
                thickness=3
            )

            # --------------------------------
            # REST
            # --------------------------------

            self.draw_text(
                frame,
                "REST",
                (
                    width // 2 - 60,
                    height // 2 - 35
                ),
                size=1.2,
                thickness=3
            )

            # --------------------------------
            # TIMER
            # --------------------------------

            self.draw_text(
                frame,
                str(remaining),
                (
                    width // 2 - 25,
                    height // 2 + 55
                ),
                size=1.6,
                thickness=3
            )

            # --------------------------------
            # NEXT SET
            # --------------------------------

            next_set = min(
                current_set,
                target_sets
            )

            self.draw_text(
                frame,
                f"NEXT: SET {next_set}",
                (
                    width // 2 - 100,
                    height // 2 + 115
                ),
                size=0.7
            )

        # =================================
        # WORKOUT COMPLETE
        # =================================

        if workout_complete:

            overlay = frame.copy()

            cv2.rectangle(
                overlay,
                (0, 0),
                (width, height),
                (0, 0, 0),
                -1
            )

            frame = cv2.addWeighted(
                overlay,
                0.75,
                frame,
                0.25,
                0
            )

            # --------------------------------
            # TITLE
            # --------------------------------

            self.draw_text(
                frame,
                "WORKOUT COMPLETE!",
                (
                    width // 2 - 220,
                    height // 2 - 100
                ),
                size=1.1,
                thickness=3
            )

            # --------------------------------
            # TOTAL REPS
            # --------------------------------

            self.draw_text(
                frame,
                f"TOTAL REPS: {total_reps}",
                (
                    width // 2 - 120,
                    height // 2 - 25
                ),
                size=0.8
            )

            # --------------------------------
            # SETS
            # --------------------------------

            self.draw_text(
                frame,
                f"SETS: {target_sets}",
                (
                    width // 2 - 70,
                    height // 2 + 20
                ),
                size=0.8
            )

            # --------------------------------
            # FORM
            # --------------------------------

            self.draw_text(
                frame,
                f"AVG FORM: {status.get('form_score', 0)}",
                (
                    width // 2 - 100,
                    height // 2 + 65
                ),
                size=0.8
            )

            # --------------------------------
            # MESSAGE
            # --------------------------------

            self.draw_text(
                frame,
                "Great job!",
                (
                    width // 2 - 80,
                    height // 2 + 125
                ),
                size=0.9,
                thickness=2
            )

        # =================================
        # READY MESSAGE
        # =================================

        if not active and not workout_complete:

            self.draw_text(
                frame,
                "Press W to start workout",
                (
                    width // 2 - 150,
                    height - 120
                ),
                size=0.7
            )

        return frame

    # ====================================
    # CONTROLS
    # ====================================

    def draw_controls(
        self,
        frame
    ):

        height = frame.shape[0]

        self.draw_text(
            frame,
            "W: Start",
            (20, height - 60),
            size=0.6
        )

        self.draw_text(
            frame,
            "S: Complete Set",
            (130, height - 60),
            size=0.6
        )

        self.draw_text(
            frame,
            "R: Reset",
            (300, height - 60),
            size=0.6
        )

        self.draw_text(
            frame,
            "Q: Quit",
            (400, height - 60),
            size=0.6
        )

        return frame

