class RepTracker:

    def __init__(self):
        self.previous_reps = 0

    def update(self, current_reps):
        """
        Detect when a new rep has been completed.
        """

        new_rep = False

        if current_reps > self.previous_reps:
            new_rep = True

        self.previous_reps = current_reps

        return new_rep

    def reset(self):
        self.previous_reps = 0