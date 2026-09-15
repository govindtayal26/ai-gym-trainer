from workout.session import WorkoutSession


workout = WorkoutSession()

workout.start_workout()

workout.add_rep()
workout.add_rep()
workout.add_rep()

workout.add_form_score(90)
workout.add_form_score(85)

workout.complete_set()

print()
print("Workout Summary")
print("----------------")
print(workout.get_summary())