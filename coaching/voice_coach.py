
import pyttsx3
import threading
import queue


class VoiceCoach:

    def __init__(self):

        # ====================================
        # SPEECH QUEUE
        # ====================================

        self.speech_queue = queue.Queue()

        # ====================================
        # CONTROL
        # ====================================

        self.running = True

        # ====================================
        # BACKGROUND THREAD
        # ====================================

        self.worker = threading.Thread(
            target=self._speech_worker,
            daemon=True
        )

        self.worker.start()

        print("Voice Coach initialized")


    # ========================================
    # SPEECH WORKER
    # ========================================

    def _speech_worker(self):

        while self.running:

            try:

                message = self.speech_queue.get(
                    timeout=0.5
                )

            except queue.Empty:

                continue

            if message is None:

                self.speech_queue.task_done()

                continue

            try:

                print(
                    f"VOICE COACH: {message}"
                )

                # --------------------------------
                # CREATE NEW ENGINE
                # --------------------------------

                engine = pyttsx3.init()

                engine.setProperty(
                    "rate",
                    175
                )

                engine.setProperty(
                    "volume",
                    1.0
                )

                # --------------------------------
                # SPEAK
                # --------------------------------

                engine.say(
                    message
                )

                engine.runAndWait()

                # --------------------------------
                # CLEANUP
                # --------------------------------

                engine.stop()

                del engine

            except Exception as error:

                print(
                    f"VOICE ERROR: {error}"
                )

            finally:

                self.speech_queue.task_done()


    # ========================================
    # SPEAK
    # ========================================

    def speak(
        self,
        message
    ):

        if not self.running:

            return

        if not message:

            return

        message = str(
            message
        ).strip()

        if not message:

            return

        print(
            f"QUEUE VOICE: {message}"
        )

        self.speech_queue.put(
            message
        )


    # ========================================
    # REP VOICE
    # ========================================

    def speak_rep(
        self,
        rep_number,
        feedback=None
    ):

        if feedback:

            message = feedback

        else:

            message = (
                f"Rep {rep_number}"
            )

        self.speak(
            message
        )


    # ========================================
    # FEEDBACK
    # ========================================

    def speak_feedback(
        self,
        feedback
    ):

        self.speak(
            feedback
        )


    # ========================================
    # SET COMPLETE
    # ========================================

    def speak_set_complete(
        self,
        rest_seconds
    ):

        message = (
            "Set complete. "
            f"Rest for "
            f"{int(rest_seconds)} "
            f"seconds."
        )

        self.speak(
            message
        )


    # ========================================
    # WORKOUT COMPLETE
    # ========================================

    def speak_workout_complete(self):

        self.speak(
            "Workout complete. Great job!"
        )


    # ========================================
    # RESET
    # ========================================

    def reset(self):

        # IMPORTANT:
        #
        # Do NOT clear the queue here.
        #
        # Otherwise messages waiting to be
        # spoken can disappear.

        pass


    # ========================================
    # STOP
    # ========================================

    def stop(self):

        if not self.running:

            return

        self.running = False

        self.speech_queue.put(
            None
        )

        print(
            "Voice Coach stopped"
        )
