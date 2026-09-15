import cv2


class WorkoutDashboard:

    def __init__(self):

        self.font = cv2.FONT_HERSHEY_SIMPLEX

    # --------------------------------
    # DRAW TEXT
    # --------------------------------

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

    # --------------------------------
    # FORMAT TIME
    # --------------------------------

    def format_duration(
        self,
        seconds
    ):

        seconds = int(seconds)

        minutes = seconds // 60

        seconds = seconds % 60

        return f"{minutes:02d}:{seconds:02d}"

    # --------------------------------
    # DRAW HEADER
    # --------------------------------

    def draw_header(
        self,
        frame
    ):

        self.draw_text(
            frame,
            "AI GYM TRAINER",
            (30, 45),
            size=1.0,
            thickness=2
        )

        self.draw_text(
            frame,
            "WORKOUT DASHBOARD",
            (30, 80),
            size=0.7,
            thickness=2
        )

    # --------------------------------
    # DRAW OVERALL STATISTICS
    # --------------------------------

    def draw_statistics(
        self,
        frame,
        statistics
    ):

        total_workouts = statistics.get(
            "total_workouts",
            0
        )

        total_reps = statistics.get(
            "total_reps",
            0
        )

        total_calories = statistics.get(
            "total_calories",
            0
        )

        average_form = statistics.get(
            "average_form",
            0
        )

        average_duration = statistics.get(
            "average_duration",
            0
        )

        self.draw_text(
            frame,
            f"WORKOUTS: {total_workouts}",
            (30, 130),
            size=0.7
        )

        self.draw_text(
            frame,
            f"TOTAL REPS: {total_reps}",
            (30, 170),
            size=0.7
        )

        self.draw_text(
            frame,
            f"CALORIES: ~{total_calories} kcal",
            (30, 210),
            size=0.7
        )

        self.draw_text(
            frame,
            f"AVG FORM: {average_form}",
            (30, 250),
            size=0.7
        )

        self.draw_text(
            frame,
            f"AVG TIME: "
            f"{self.format_duration(average_duration)}",
            (30, 290),
            size=0.7
        )

    # --------------------------------
    # DRAW EXERCISE STATISTICS
    # --------------------------------

    def draw_exercise_statistics(
        self,
        frame,
        exercise_statistics
    ):

        self.draw_text(
            frame,
            "EXERCISE STATISTICS",
            (450, 130),
            size=0.75,
            thickness=2
        )

        y = 175

        for exercise, stats in (
            exercise_statistics.items()
        ):

            workouts = stats.get(
                "workouts",
                0
            )

            reps = stats.get(
                "reps",
                0
            )

            calories = stats.get(
                "calories",
                0
            )

            form = stats.get(
                "average_form",
                0
            )

            self.draw_text(
                frame,
                exercise,
                (450, y),
                size=0.7
            )

            self.draw_text(
                frame,
                f"Workouts: {workouts}",
                (450, y + 30),
                size=0.55
            )

            self.draw_text(
                frame,
                f"Reps: {reps}",
                (450, y + 55),
                size=0.55
            )

            self.draw_text(
                frame,
                f"Calories: ~{calories}",
                (450, y + 80),
                size=0.55
            )

            self.draw_text(
                frame,
                f"Form: {form}",
                (450, y + 105),
                size=0.55
            )

            y += 145

    # --------------------------------
    # DRAW RECENT WORKOUTS
    # --------------------------------

    def draw_recent_workouts(
        self,
        frame,
        workouts
    ):

        height = frame.shape[0]

        self.draw_text(
            frame,
            "RECENT WORKOUTS",
            (30, height - 240),
            size=0.75,
            thickness=2
        )

        y = height - 200

        for workout in workouts[:5]:

            workout_id = workout.get(
                "id",
                0
            )

            exercise = workout.get(
                "exercise",
                "Unknown"
            )

            reps = workout.get(
                "total_reps",
                0
            )

            duration = workout.get(
                "duration_seconds",
                0
            )

            form = workout.get(
                "average_form_score",
                0
            )

            calories = workout.get(
                "calories_burned",
                0
            )

            text = (
                f"#{workout_id}  "
                f"{exercise}  "
                f"{reps} reps  "
                f"{self.format_duration(duration)}  "
                f"~{calories} kcal  "
                f"Form {form}"
            )

            self.draw_text(
                frame,
                text,
                (30, y),
                size=0.52
            )

            y += 30

    # --------------------------------
    # DRAW CONTROLS
    # --------------------------------

    def draw_controls(
        self,
        frame
    ):

        height = frame.shape[0]

        self.draw_text(
            frame,
            "D: Dashboard",
            (30, height - 30),
            size=0.55
        )

        self.draw_text(
            frame,
            "W: Workout",
            (180, height - 30),
            size=0.55
        )

        self.draw_text(
            frame,
            "Q: Quit",
            (330, height - 30),
            size=0.55
        )

    # --------------------------------
    # DRAW DASHBOARD
    # --------------------------------

    def draw(
        self,
        frame,
        statistics,
        exercise_statistics,
        recent_workouts
    ):

        self.draw_header(frame)

        self.draw_statistics(
            frame,
            statistics
        )

        self.draw_exercise_statistics(
            frame,
            exercise_statistics
        )

        self.draw_recent_workouts(
            frame,
            recent_workouts
        )

        self.draw_controls(frame)

        return frame