from workout.manager import WorkoutManager


workout = WorkoutManager()


workout.start()

workout.add_rep(90)
workout.add_rep(85)
workout.add_rep(95)

print("Current status:")
print(workout.get_status())


workout.complete_set()

print()
print("Workout summary:")
print(workout.get_summary())