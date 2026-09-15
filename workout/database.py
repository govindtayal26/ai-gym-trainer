
import sqlite3
from datetime import datetime


class WorkoutDatabase:

    def __init__(
        self,
        database_name="workout_history.db"
    ):

        self.database_name = database_name

        self.connection = None

        self.connect()

        self.create_tables()

    # ========================================
    # CONNECT DATABASE
    # ========================================

    def connect(self):

        self.connection = sqlite3.connect(
            self.database_name
        )

        self.connection.row_factory = (
            sqlite3.Row
        )

    # ========================================
    # CREATE TABLE
    # ========================================

    def create_tables(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS workouts (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                exercise TEXT NOT NULL,

                total_sets INTEGER DEFAULT 0,

                total_reps INTEGER DEFAULT 0,

                average_form_score REAL DEFAULT 0,

                duration_seconds REAL DEFAULT 0,

                completed INTEGER DEFAULT 0,

                created_at TEXT NOT NULL

            )
            """
        )

        self.connection.commit()

    # ========================================
    # SAVE WORKOUT
    # ========================================

    def save_workout(
        self,
        exercise,
        total_sets,
        total_reps,
        average_form_score,
        duration_seconds,
        completed
    ):

        cursor = self.connection.cursor()

        created_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor.execute(
            """
            INSERT INTO workouts (

                exercise,
                total_sets,
                total_reps,
                average_form_score,
                duration_seconds,
                completed,
                created_at

            )

            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,

            (
                exercise,
                total_sets,
                total_reps,
                average_form_score,
                duration_seconds,
                int(completed),
                created_at
            )
        )

        self.connection.commit()

        return cursor.lastrowid

    # ========================================
    # GET ALL WORKOUTS
    # ========================================

    def get_all_workouts(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *

            FROM workouts

            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        return [
            dict(row)
            for row in rows
        ]

    # ========================================
    # GET RECENT WORKOUTS
    # ========================================

    def get_recent_workouts(
        self,
        limit=10
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *

            FROM workouts

            ORDER BY id DESC

            LIMIT ?
            """,
            (limit,)
        )

        rows = cursor.fetchall()

        return [
            dict(row)
            for row in rows
        ]

    # ========================================
    # GET ONE WORKOUT
    # ========================================

    def get_workout(
        self,
        workout_id
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT *

            FROM workouts

            WHERE id = ?
            """,
            (workout_id,)
        )

        row = cursor.fetchone()

        if row is None:

            return None

        return dict(row)

    # ========================================
    # TOTAL WORKOUTS
    # ========================================

    def get_total_workouts(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) AS total

            FROM workouts
            """
        )

        row = cursor.fetchone()

        return row["total"]

    # ========================================
    # TOTAL REPS
    # ========================================

    def get_total_reps(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT COALESCE(
                SUM(total_reps),
                0
            ) AS total

            FROM workouts
            """
        )

        row = cursor.fetchone()

        return row["total"]

    # ========================================
    # AVERAGE FORM SCORE
    # ========================================

    def get_average_form_score(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT COALESCE(
                AVG(average_form_score),
                0
            ) AS average

            FROM workouts

            WHERE completed = 1
            """
        )

        row = cursor.fetchone()

        return round(
            row["average"],
            1
        )

    # ========================================
    # EXERCISE STATISTICS
    # ========================================

    def get_exercise_statistics(
        self,
        exercise
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT

                COUNT(*) AS workouts,

                COALESCE(
                    SUM(total_reps),
                    0
                ) AS reps,

                COALESCE(
                    AVG(average_form_score),
                    0
                ) AS average_form

            FROM workouts

            WHERE exercise = ?
            """,
            (exercise,)
        )

        row = cursor.fetchone()

        return {

            "workouts":
                row["workouts"],

            "reps":
                row["reps"],

            "average_form":
                round(
                    row["average_form"],
                    1
                )
        }

    # ========================================
    # DELETE WORKOUT
    # ========================================

    def delete_workout(
        self,
        workout_id
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            DELETE FROM workouts

            WHERE id = ?
            """,
            (workout_id,)
        )

        self.connection.commit()

        return (
            cursor.rowcount > 0
        )

    # ========================================
    # CLOSE DATABASE
    # ========================================

    def close(self):

        if self.connection is not None:

            self.connection.close()

            self.connection = None

