from collections import deque


class ExerciseStabilizer:

    def __init__(
        self,
        history_size=15,
        minimum_votes=8
    ):

        # ========================================
        # SETTINGS
        # ========================================

        self.history_size = history_size

        self.minimum_votes = minimum_votes

        # Minimum number of frames required
        # before making a decision.

        self.minimum_history = 5

        # ========================================
        # HISTORY
        # ========================================

        self.history = deque(
            maxlen=self.history_size
        )

        # ========================================
        # CURRENT EXERCISE
        # ========================================

        self.current_exercise = "Unknown"

        # ========================================
        # CANDIDATE EXERCISE
        # ========================================

        self.candidate_exercise = "Unknown"

        self.candidate_count = 0

    # ========================================
    # UPDATE
    # ========================================

    def update(self, detected_exercise):

        # ----------------------------------------
        # PROTECT AGAINST NONE
        # ----------------------------------------

        if detected_exercise is None:

            detected_exercise = "Unknown"

        # ----------------------------------------
        # ADD TO HISTORY
        # ----------------------------------------

        self.history.append(
            detected_exercise
        )

        # ----------------------------------------
        # NOT ENOUGH HISTORY
        # ----------------------------------------

        if len(self.history) < self.minimum_history:

            return self.current_exercise

        # ========================================
        # COUNT VOTES
        # ========================================

        counts = {}

        for exercise in self.history:

            counts[exercise] = (
                counts.get(
                    exercise,
                    0
                )
                + 1
            )

        # ========================================
        # REMOVE UNKNOWN
        # ========================================

        known_counts = {

            exercise: count

            for exercise, count
            in counts.items()

            if exercise != "Unknown"
        }

        # If everything is Unknown,
        # keep the previous exercise.

        if not known_counts:

            return self.current_exercise

        # ========================================
        # FIND BEST EXERCISE
        # ========================================

        best_exercise = max(
            known_counts,
            key=known_counts.get
        )

        best_count = known_counts[
            best_exercise
        ]

        # ========================================
        # MINIMUM VOTES
        # ========================================

        if best_count < self.minimum_votes:

            return self.current_exercise

        # ========================================
        # SAME EXERCISE
        # ========================================

        if (
            best_exercise
            ==
            self.current_exercise
        ):

            self.candidate_exercise = "Unknown"

            self.candidate_count = 0

            return self.current_exercise

        # ========================================
        # NEW CANDIDATE
        # ========================================

        if (
            best_exercise
            !=
            self.candidate_exercise
        ):

            self.candidate_exercise = (
                best_exercise
            )

            self.candidate_count = 1

            return self.current_exercise

        # ========================================
        # CANDIDATE CONTINUES
        # ========================================

        self.candidate_count += 1

        # ========================================
        # CONFIRM NEW EXERCISE
        # ========================================

        if self.candidate_count >= 3:

            self.current_exercise = (
                self.candidate_exercise
            )

            self.candidate_exercise = "Unknown"

            self.candidate_count = 0

        return self.current_exercise

    # ========================================
    # GET CURRENT EXERCISE
    # ========================================

    def get_current_exercise(self):

        return self.current_exercise

    # ========================================
    # GET HISTORY
    # ========================================

    def get_history(self):

        return list(
            self.history
        )

    # ========================================
    # GET VOTE COUNTS
    # ========================================

    def get_vote_counts(self):

        counts = {}

        for exercise in self.history:

            counts[exercise] = (
                counts.get(
                    exercise,
                    0
                )
                + 1
            )

        return counts

    # ========================================
    # RESET
    # ========================================

    def reset(self):

        self.history.clear()

        self.current_exercise = "Unknown"

        self.candidate_exercise = "Unknown"

        self.candidate_count = 0