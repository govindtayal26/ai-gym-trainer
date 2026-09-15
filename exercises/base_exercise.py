from abc import ABC, abstractmethod


class BaseExercise(ABC):

    def __init__(self):
        self.reps = 0
        self.stage = "up"
        self.form_score = 0
        self.feedback = "Get ready"

    @abstractmethod
    def update(self, landmarks):
        """
        Process body landmarks and update
        reps, form score and feedback.
        """
        pass

    def get_result(self):

        return {
            "reps": self.reps,
            "stage": self.stage,
            "form_score": self.form_score,
            "feedback": self.feedback
        }

    def reset(self):

        self.reps = 0
        self.stage = "up"
        self.form_score = 0
        self.feedback = "Get ready"