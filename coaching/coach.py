
class AICoach:

    def __init__(self):

        # ====================================
        # CURRENT FEEDBACK
        # ====================================

        self.last_feedback = "Get ready"

        # ====================================
        # FEEDBACK HISTORY
        # ====================================

        self.feedback_history = []

        self.max_history = 5

        # ====================================
        # REP TRACKING
        # ====================================

        self.last_reps = 0

        # ====================================
        # COACHING STATE
        # ====================================

        self.last_exercise = "Unknown"

        self.last_form_score = 0

        self.last_stage = "unknown"

        # ====================================
        # FEEDBACK CHANGE TRACKING
        # ====================================

        self.same_feedback_count = 0


    # ========================================
    # UPDATE FEEDBACK
    # ========================================

    def update(
        self,
        exercise,
        result
    ):

        if result is None:

            return "No feedback"


        # ====================================
        # READ RESULT
        # ====================================

        reps = result.get(
            "reps",
            0
        )

        stage = result.get(
            "stage",
            "unknown"
        )

        form_score = result.get(
            "form_score",
            0
        )

        exercise_feedback = result.get(
            "feedback",
            "Keep going"
        )


        # ====================================
        # EXERCISE CHANGE
        # ====================================

        if exercise != self.last_exercise:

            self.feedback_history = []

            self.last_feedback = "Get ready"

            self.last_reps = 0

            self.same_feedback_count = 0

            self.last_exercise = exercise


        # ====================================
        # SAVE STATE
        # ====================================

        self.last_form_score = form_score

        self.last_stage = stage


        # ====================================
        # GENERATE SMART FEEDBACK
        # ====================================

        feedback = self.generate_feedback(

            exercise=exercise,

            reps=reps,

            stage=stage,

            form_score=form_score,

            exercise_feedback=exercise_feedback
        )


        # ====================================
        # FEEDBACK HISTORY
        # ====================================

        self.feedback_history.append(
            feedback
        )


        if (
            len(self.feedback_history)
            >
            self.max_history
        ):

            self.feedback_history.pop(0)


        # ====================================
        # STABILIZE
        # ====================================

        self.last_feedback = (
            self.get_stable_feedback()
        )


        # ====================================
        # UPDATE REP
        # ====================================

        self.last_reps = reps


        return self.last_feedback


    # ========================================
    # SMART FEEDBACK GENERATOR
    # ========================================

    def generate_feedback(

        self,

        exercise,

        reps,

        stage,

        form_score,

        exercise_feedback

    ):

        # ====================================
        # NO EXERCISE
        # ====================================

        if exercise == "Unknown":

            return "Get ready"


        # ====================================
        # NO PERSON / INVALID
        # ====================================

        if (
            exercise_feedback
            ==
            "No person detected"
        ):

            return "Position yourself in front of the camera"


        # ====================================
        # VERY LOW FORM
        # ====================================

        if form_score < 30:

            return exercise_feedback


        # ====================================
        # BICEP CURL
        # ====================================

        if exercise == "Bicep Curl":

            return self.bicep_coaching(

                reps,

                stage,

                form_score,

                exercise_feedback
            )


        # ====================================
        # SQUAT
        # ====================================

        if exercise == "Squat":

            return self.squat_coaching(

                reps,

                stage,

                form_score,

                exercise_feedback
            )


        # ====================================
        # PUSH-UP
        # ====================================

        if exercise == "Push-up":

            return self.pushup_coaching(

                reps,

                stage,

                form_score,

                exercise_feedback
            )


        # ====================================
        # GENERAL
        # ====================================

        return self.general_coaching(

            reps,

            form_score,

            exercise_feedback
        )


    # ========================================
    # BICEP COACHING
    # ========================================

    def bicep_coaching(

        self,

        reps,

        stage,

        form_score,

        feedback

    ):

        if "elbow" in feedback.lower():

            return feedback


        if "higher" in feedback.lower():

            return feedback


        if "extend" in feedback.lower():

            return feedback


        if "too far" in feedback.lower():

            return feedback


        if form_score >= 90:

            return "Excellent curl"


        if form_score >= 75:

            return "Good form"


        if form_score >= 60:

            return "Good. Stay controlled"


        return feedback


    # ========================================
    # SQUAT COACHING
    # ========================================

    def squat_coaching(

        self,

        reps,

        stage,

        form_score,

        feedback

    ):

        if "knee" in feedback.lower():

            return feedback


        if "deeper" in feedback.lower():

            return feedback


        if "chest" in feedback.lower():

            return feedback


        if form_score >= 90:

            return "Excellent squat"


        if form_score >= 75:

            return "Good squat form"


        if form_score >= 60:

            return "Good. Stay controlled"


        return feedback


    # ========================================
    # PUSH-UP COACHING
    # ========================================

    def pushup_coaching(

        self,

        reps,

        stage,

        form_score,

        feedback

    ):

        feedback_lower = feedback.lower()


        if "body" in feedback_lower:

            return feedback


        if "lower" in feedback_lower:

            return feedback


        if "elbow" in feedback_lower:

            return feedback


        if form_score >= 90:

            return "Excellent push-up"


        if form_score >= 75:

            return "Good push-up form"


        if form_score >= 60:

            return "Good. Stay controlled"


        return feedback


    # ========================================
    # GENERAL COACHING
    # ========================================

    def general_coaching(

        self,

        reps,

        form_score,

        feedback

    ):

        if form_score >= 90:

            return "Excellent form"


        if form_score >= 75:

            return "Good form"


        if form_score >= 60:

            return "Keep going"


        return feedback


    # ========================================
    # STABLE FEEDBACK
    # ========================================

    def get_stable_feedback(self):

        if not self.feedback_history:

            return self.last_feedback


        # ====================================
        # COUNT FEEDBACK
        # ====================================

        counts = {}


        for feedback in self.feedback_history:

            counts[feedback] = (
                counts.get(
                    feedback,
                    0
                )
                + 1
            )


        # ====================================
        # MOST COMMON
        # ====================================

        best_feedback = max(

            counts,

            key=counts.get
        )


        return best_feedback


    # ========================================
    # GET CURRENT FEEDBACK
    # ========================================

    def get_feedback(self):

        return self.last_feedback


    # ========================================
    # GET FEEDBACK TYPE
    # ========================================

    def get_feedback_type(self):

        feedback = (
            self.last_feedback
            .lower()
        )


        # ====================================
        # POSITIVE
        # ====================================

        positive_words = [

            "excellent",

            "good",

            "great",

            "perfect",

            "strong",

            "well done"
        ]


        for word in positive_words:

            if word in feedback:

                return "positive"


        # ====================================
        # NEUTRAL
        # ====================================

        neutral_words = [

            "get ready",

            "keep going",

            "stay controlled",

            "position yourself"
        ]


        for word in neutral_words:

            if word in feedback:

                return "neutral"


        # ====================================
        # WARNING
        # ====================================

        return "warning"


    # ========================================
    # GET REP
    # ========================================

    def get_reps(self):

        return self.last_reps


    # ========================================
    # GET FORM SCORE
    # ========================================

    def get_form_score(self):

        return self.last_form_score


    # ========================================
    # GET STAGE
    # ========================================

    def get_stage(self):

        return self.last_stage


    # ========================================
    # RESET
    # ========================================

    def reset(self):

        self.last_feedback = "Get ready"

        self.feedback_history = []

        self.last_reps = 0

        self.last_exercise = "Unknown"

        self.last_form_score = 0

        self.last_stage = "unknown"

        self.same_feedback_count = 0
