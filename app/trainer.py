import cv2

from camera import Camera
from pose_detector import PoseDetector

from recognition.exercise_detector import ExerciseDetector
from recognition.exercise_stabilizer import ExerciseStabilizer

from exercises.exercise_manager import ExerciseManager

from workout.app import WorkoutApp
from workout.dashboard import WorkoutDashboard
from workout.settings_ui import SettingsUI

from coaching.coach import AICoach
from coaching.voice_coach import VoiceCoach


class Trainer:

    def __init__(self):

        # ========================================
        # CAMERA
        # ========================================

        self.camera = Camera()

        # ========================================
        # POSE DETECTION
        # ========================================

        self.pose_detector = PoseDetector()

        # ========================================
        # EXERCISE RECOGNITION
        # ========================================

        self.exercise_detector = (
            ExerciseDetector()
        )

        self.exercise_stabilizer = (
            ExerciseStabilizer()
        )

        # ========================================
        # EXERCISE MANAGER
        # ========================================

        self.exercise_manager = (
            ExerciseManager()
        )

        # ========================================
        # WORKOUT SYSTEM
        # ========================================

        self.workout = WorkoutApp()

        # ========================================
        # AI COACH
        # ========================================

        self.coach = AICoach()

        # ========================================
        # VOICE COACH
        # ========================================

        self.voice_coach = VoiceCoach()

        # ========================================
        # SETTINGS
        # ========================================

        self.settings_ui = SettingsUI()

        self.show_settings = True

        # ========================================
        # DASHBOARD
        # ========================================

        self.dashboard = WorkoutDashboard()

        self.show_dashboard = False

        # ========================================
        # APPLICATION STATE
        # ========================================

        self.exercise_name = "Unknown"

        self.result = self.default_result(
            "Get ready"
        )

        # ========================================
        # SET TRACKING
        # ========================================

        self.previous_completed_sets = 0

        # ========================================
        # VOICE TRACKING
        # ========================================

        self.previous_voice_reps = 0

        self.workout_complete_voice_sent = False

        # ========================================
        # APPLICATION STATUS
        # ========================================

        self.running = False

    # ========================================
    # DEFAULT RESULT
    # ========================================

    def default_result(
        self,
        feedback="Get ready"
    ):

        return {

            "exercise":
                self.exercise_name,

            "reps":
                0,

            "stage":
                "unknown",

            "form_score":
                0,

            "feedback":
                feedback
        }

    # ========================================
    # START APPLICATION
    # ========================================

    def start(self):

        self.camera.start()

        self.running = True

        print(
            "AI Gym Trainer started"
        )

    # ========================================
    # PROCESS FRAME
    # ========================================

    def process_frame(
        self,
        frame
    ):

        # ====================================
        # SETTINGS MODE
        # ====================================

        if self.show_settings:

            return self.settings_ui.draw(
                frame
            )

        # ====================================
        # DASHBOARD MODE
        # ====================================

        if self.show_dashboard:

            return self.show_workout_dashboard(
                frame
            )

        # ====================================
        # POSE DETECTION
        # ====================================

        results = (
            self.pose_detector.detect(
                frame
            )
        )

        # ====================================
        # DRAW POSE
        # ====================================

        frame = (
            self.pose_detector
            .draw_landmarks(
                frame,
                results
            )
        )

        # ====================================
        # GET LANDMARKS
        # ====================================

        landmarks = (
            self.pose_detector
            .get_landmarks(
                results
            )
        )

        # ====================================
        # NO PERSON DETECTED
        # ====================================

        if landmarks is None:

            return self.process_no_person(
                frame
            )

        # ====================================
        # EXERCISE RECOGNITION
        # ====================================

        detected_exercise = (
            self.detect_exercise(
                landmarks
            )
        )

        # ====================================
        # HANDLE EXERCISE
        # ====================================

        self.handle_exercise_change(
            detected_exercise
        )

        # ====================================
        # EXERCISE ANALYSIS
        # ====================================

        self.update_exercise(
            landmarks
        )

        # ====================================
        # UPDATE WORKOUT
        # ====================================

        self.update_workout()

        # ====================================
        # CHECK SET
        # ====================================

        status = (
            self.workout.get_status()
        )

        self.handle_set_completion(
            status
        )

        # ====================================
        # CHECK WORKOUT COMPLETE
        # ====================================

        self.handle_workout_completion()

        # ====================================
        # DRAW UI
        # ====================================

        status = (
            self.workout.get_status()
        )

        frame = self.draw_workout_ui(
            frame,
            status
        )

        return frame

    # ========================================
    # NO PERSON HANDLER
    # ========================================

    def process_no_person(
        self,
        frame
    ):

        self.result = self.default_result(
            "No person detected"
        )

        status = (
            self.workout.get_status()
        )

        frame = (
            self.workout.ui
            .draw_status(

                frame,

                status,

                self.exercise_name,

                self.result[
                    "form_score"
                ],

                self.result[
                    "reps"
                ]
            )
        )

        frame = (
            self.workout.ui
            .draw_controls(
                frame
            )
        )

        return frame

    # ========================================
    # EXERCISE DETECTION
    # ========================================

    def detect_exercise(
        self,
        landmarks
    ):

        detected_exercise = (
            self.exercise_detector
            .detect(
                landmarks
            )
        )

        stable_exercise = (
            self.exercise_stabilizer
            .update(
                detected_exercise
            )
        )

        return stable_exercise

    # ========================================
    # HANDLE EXERCISE CHANGE
    # ========================================

    def handle_exercise_change(
        self,
        detected_exercise
    ):

        # Ignore temporary Unknown
        # detections.

        if (
            detected_exercise is None
            or
            detected_exercise == "Unknown"
        ):

            return

        # Same exercise.
        if (
            detected_exercise
            ==
            self.exercise_name
        ):

            return

        # ====================================
        # NEW EXERCISE
        # ====================================

        print(
            f"\nExercise changed: "
            f"{self.exercise_name} "
            f"-> "
            f"{detected_exercise}"
        )

        self.exercise_name = (
            detected_exercise
        )

        # ====================================
        # UPDATE EXERCISE MANAGER
        # ====================================

        self.exercise_manager.set_exercise(
            self.exercise_name
        )

        # ====================================
        # RESET EXERCISE STATE
        # ====================================

        self.exercise_manager.reset()

        # ====================================
        # RESET TRACKING
        # ====================================

        self.previous_voice_reps = 0

        self.previous_completed_sets = (
            0
        )

        self.workout_complete_voice_sent = (
            False
        )

        # ====================================
        # RESET COACH
        # ====================================

        self.coach.reset()

        # ====================================
        # RESET VOICE COACH
        # ====================================

        self.voice_coach.reset()

        # ====================================
        # RESET DISPLAY
        # ====================================

        self.result = self.default_result(
            "Get ready"
        )

    # ========================================
    # UPDATE EXERCISE
    # ========================================

    def update_exercise(
        self,
        landmarks
    ):

        # No exercise selected.
        if (
            self.exercise_name
            ==
            "Unknown"
        ):

            self.result = self.default_result(
                "Select an exercise"
            )

            return

        # ====================================
        # EXERCISE ENGINE
        # ====================================

        self.result = (
            self.exercise_manager
            .update(
                landmarks
            )
        )

        # ====================================
        # AI COACH
        # ====================================

        coach_feedback = (
            self.coach.update(
                self.exercise_name,
                self.result
            )
        )

        self.result["feedback"] = (
            coach_feedback
        )

        # ====================================
        # VOICE REP TRACKING
        # ====================================

        current_reps = int(
            self.result.get(
                "reps",
                0
            )
        )

        # ====================================
        # NEW REP
        # ====================================

        if (
            current_reps
            >
            self.previous_voice_reps
        ):

            print(
                f"\nVOICE REP: "
                f"{current_reps}"
            )

            self.voice_coach.speak_rep(

                current_reps,

                coach_feedback
            )

            self.previous_voice_reps = (
                current_reps
            )

    # ========================================
    # UPDATE WORKOUT
    # ========================================

    def update_workout(self):

        self.workout.update(

            exercise=self.exercise_name,

            reps=self.result.get(
                "reps",
                0
            ),

            form_score=self.result.get(
                "form_score",
                0
            )
        )

    # ========================================
    # HANDLE SET COMPLETION
    # ========================================

    def handle_set_completion(
        self,
        status
    ):

        current_completed_sets = int(
            status.get(
                "total_sets",
                0
            )
        )

        # ====================================
        # NO NEW SET
        # ====================================

        if (
            current_completed_sets
            <=
            self.previous_completed_sets
        ):

            return

        # ====================================
        # SAVE SET COUNT
        # ====================================

        self.previous_completed_sets = (
            current_completed_sets
        )

        # ====================================
        # VOICE
        # ====================================

        rest_remaining = int(
            status.get(
                "rest_remaining",
                0
            )
        )

        self.voice_coach.speak_set_complete(
            rest_remaining
        )

        # ====================================
        # RESET EXERCISE
        # ====================================

        self.exercise_manager.reset()

        # ====================================
        # KEEP CURRENT EXERCISE
        # ====================================

        if (
            self.exercise_name
            !=
            "Unknown"
        ):

            self.exercise_manager.set_exercise(
                self.exercise_name
            )

        # ====================================
        # RESET COACH
        # ====================================

        self.coach.reset()

        # ====================================
        # RESET REP VOICE
        # ====================================

        self.previous_voice_reps = 0

        # ====================================
        # RESET RESULT
        # ====================================

        self.result = self.default_result(
            "Get ready for next set"
        )

        print(
            f"\nSET COMPLETE: "
            f"{current_completed_sets}"
        )

    # ========================================
    # WORKOUT COMPLETION
    # ========================================

    def handle_workout_completion(self):

        if not self.workout.is_complete():

            return

        if self.workout_complete_voice_sent:

            return

        self.voice_coach.speak_workout_complete()

        self.workout_complete_voice_sent = (
            True
        )

        print(
            "\nWORKOUT COMPLETE"
        )

    # ========================================
    # DRAW WORKOUT UI
    # ========================================

    def draw_workout_ui(
        self,
        frame,
        status
    ):

        # ====================================
        # MAIN STATUS UI
        # ====================================

        frame = (
            self.workout.ui
            .draw_status(

                frame,

                status,

                self.exercise_name,

                self.result.get(
                    "form_score",
                    0
                ),

                self.result.get(
                    "reps",
                    0
                )
            )
        )

        # ====================================
        # CONTROLS
        # ====================================

        frame = (
            self.workout.ui
            .draw_controls(
                frame
            )
        )

        # ====================================
        # COACH FEEDBACK
        # ====================================

        feedback = self.result.get(
            "feedback",
            "Get ready"
        )

        feedback_type = (
            self.coach
            .get_feedback_type()
        )

        # ====================================
        # FEEDBACK POSITION
        # ====================================

        feedback_y = 440

        height, width = (
            frame.shape[:2]
        )

        # ====================================
        # FEEDBACK BOX
        # ====================================

        cv2.rectangle(

            frame,

            (
                10,
                feedback_y - 35
            ),

            (
                min(
                    width - 10,
                    650
                ),
                feedback_y + 10
            ),

            (20, 20, 20),

            -1
        )

        # ====================================
        # COACH TITLE
        # ====================================

        cv2.putText(

            frame,

            "AI COACH:",

            (
                20,
                feedback_y
            ),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.65,

            (0, 255, 255),

            2,

            cv2.LINE_AA
        )

        # ====================================
        # FEEDBACK COLOR
        # ====================================

        if (
            feedback_type
            ==
            "positive"
        ):

            feedback_color = (
                0,
                255,
                0
            )

        elif (
            feedback_type
            ==
            "warning"
        ):

            feedback_color = (
                0,
                165,
                255
            )

        else:

            feedback_color = (
                255,
                255,
                255
            )

        # ====================================
        # FEEDBACK TEXT
        # ====================================

        # Prevent extremely long feedback
        # from overflowing the UI.

        feedback_text = str(
            feedback
        )

        if len(feedback_text) > 65:

            feedback_text = (
                feedback_text[:62]
                +
                "..."
            )

        cv2.putText(

            frame,

            feedback_text,

            (
                145,
                feedback_y
            ),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.65,

            feedback_color,

            2,

            cv2.LINE_AA
        )

        # ====================================
        # DETECTED EXERCISE
        # ====================================

        cv2.putText(

            frame,

            f"Detected: "
            f"{self.exercise_name}",

            (
                20,
                480
            ),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (255, 255, 0),

            2,

            cv2.LINE_AA
        )

        # ====================================
        # SET REPS
        # ====================================

        cv2.putText(

            frame,

            f"SET REPS: "
            f"{self.result.get('reps', 0)}",

            (
                20,
                520
            ),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (0, 255, 255),

            2,

            cv2.LINE_AA
        )

        # ====================================
        # TOTAL REPS
        # ====================================

        cv2.putText(

            frame,

            f"TOTAL REPS: "
            f"{status.get('total_reps', 0)}",

            (
                20,
                560
            ),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (0, 255, 255),

            2,

            cv2.LINE_AA
        )

        return frame

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

        # ====================================
        # WORKOUT CONFIG
        # ====================================

        self.workout.configure_workout(

            exercise=exercise,

            target_reps=target_reps,

            target_sets=target_sets,

            rest_seconds=rest_seconds,

            weight_kg=weight_kg
        )

        # ====================================
        # EXERCISE
        # ====================================

        self.exercise_name = exercise

        self.exercise_manager.set_exercise(
            exercise
        )

        # ====================================
        # RESET RECOGNITION
        # ====================================

        self.exercise_detector.current_exercise = (
            "Unknown"
        )

        self.exercise_stabilizer.reset()

        # ====================================
        # RESET TRACKING
        # ====================================

        self.previous_completed_sets = 0

        self.previous_voice_reps = 0

        self.workout_complete_voice_sent = (
            False
        )

        # ====================================
        # RESET COACH
        # ====================================

        self.coach.reset()

        # ====================================
        # RESET VOICE
        # ====================================

        self.voice_coach.reset()

        # ====================================
        # RESET RESULT
        # ====================================

        self.result = self.default_result(
            "Get ready"
        )

    # ========================================
    # GET CONFIG
    # ========================================

    def get_config(self):

        return (
            self.workout
            .get_config()
        )

    # ========================================
    # HANDLE SETTINGS KEY
    # ========================================

    def handle_settings_key(
        self,
        key
    ):

        # ====================================
        # QUIT
        # ====================================

        if key == ord("q"):

            return False

        # ====================================
        # START WORKOUT
        # ====================================

        if key == 13:

            config = (
                self.settings_ui
                .get_config()
            )

            self.configure_workout(
                **config
            )

            self.show_settings = False

            self.show_dashboard = False

            self.start_workout()

            return True

        # ====================================
        # SETTINGS NAVIGATION
        # ====================================

        self.settings_ui.handle_key(
            key
        )

        return True

    # ========================================
    # START WORKOUT
    # ========================================

    def start_workout(self):

        self.workout.start_workout()

        # ====================================
        # RESET RECOGNITION
        # ====================================

        self.exercise_detector.current_exercise = (
            "Unknown"
        )

        self.exercise_stabilizer.reset()

        # ====================================
        # RESET TRACKING
        # ====================================

        self.previous_completed_sets = 0

        self.previous_voice_reps = 0

        self.workout_complete_voice_sent = (
            False
        )

        # ====================================
        # RESET EXERCISE
        # ====================================

        self.exercise_manager.reset()

        # ====================================
        # KEEP SELECTED EXERCISE
        # ====================================

        if (
            self.exercise_name
            !=
            "Unknown"
        ):

            self.exercise_manager.set_exercise(
                self.exercise_name
            )

        # ====================================
        # RESET COACH
        # ====================================

        self.coach.reset()

        # ====================================
        # RESET VOICE
        # ====================================

        self.voice_coach.reset()

        # ====================================
        # RESET RESULT
        # ====================================

        self.result = self.default_result(
            "Get ready"
        )

        print(
            "Workout session started"
        )

    # ========================================
    # COMPLETE SET
    # ========================================

    def complete_set(self):

        result = (
            self.workout
            .complete_set()
        )

        status = (
            self.workout
            .get_status()
        )

        self.previous_completed_sets = (
            status.get(
                "total_sets",
                0
            )
        )

        self.previous_voice_reps = 0

        return result

    # ========================================
    # RESET APPLICATION
    # ========================================

    def reset(self):

        # ====================================
        # WORKOUT
        # ====================================

        self.workout.reset()

        # ====================================
        # EXERCISE
        # ====================================

        self.exercise_manager.reset()

        # ====================================
        # RECOGNITION
        # ====================================

        self.exercise_detector.current_exercise = (
            "Unknown"
        )

        self.exercise_stabilizer.reset()

        # ====================================
        # COACH
        # ====================================

        self.coach.reset()

        self.voice_coach.reset()

        # ====================================
        # STATE
        # ====================================

        self.exercise_name = "Unknown"

        self.previous_completed_sets = 0

        self.previous_voice_reps = 0

        self.workout_complete_voice_sent = (
            False
        )

        # ====================================
        # UI
        # ====================================

        self.show_dashboard = False

        self.show_settings = True

        self.settings_ui.reset()

        # ====================================
        # RESULT
        # ====================================

        self.result = self.default_result(
            "Get ready"
        )

    # ========================================
    # SAVE WORKOUT
    # ========================================

    def save_workout(self):

        return (
            self.workout
            .save_workout()
        )

    # ========================================
    # GET SUMMARY
    # ========================================

    def get_summary(self):

        return (
            self.workout
            .get_summary()
        )

    # ========================================
    # GET HISTORY
    # ========================================

    def get_history(
        self,
        limit=10
    ):

        return (
            self.workout
            .get_history(
                limit
            )
        )

    # ========================================
    # DASHBOARD
    # ========================================

    def show_workout_dashboard(
        self,
        frame
    ):

        statistics = (
            self.workout
            .get_dashboard_statistics()
        )

        exercise_statistics = (
            self.workout
            .get_dashboard_exercises()
        )

        recent_workouts = (
            self.workout
            .get_dashboard_history()
        )

        return (
            self.dashboard.draw(

                frame,

                statistics,

                exercise_statistics,

                recent_workouts
            )
        )

    # ========================================
    # TOGGLE DASHBOARD
    # ========================================

    def toggle_dashboard(self):

        self.show_dashboard = (
            not self.show_dashboard
        )

    # ========================================
    # STOP
    # ========================================

    def stop(self):

        if not self.running:

            # Still release resources in case
            # start() was never called.

            self.camera.release()

            self.pose_detector.close()

            self.voice_coach.stop()

            self.workout.close()

            return

        self.running = False

        # ====================================
        # RELEASE CAMERA
        # ====================================

        self.camera.release()

        # ====================================
        # CLOSE POSE
        # ====================================

        self.pose_detector.close()

        # ====================================
        # STOP VOICE
        # ====================================

        self.voice_coach.stop()

        # ====================================
        # CLOSE DATABASE
        # ====================================

        self.workout.close()

        print(
            "AI Gym Trainer stopped"
        )