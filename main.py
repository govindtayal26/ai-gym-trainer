
import cv2

from app.trainer import Trainer


def main():

    # ========================================
    # CREATE TRAINER
    # ========================================

    trainer = Trainer()

    # ========================================
    # START TRAINER
    # ========================================

    trainer.start()

    print()
    print("========================================")
    print("       AI GYM TRAINER")
    print("========================================")
    print()
    print("SETTINGS:")
    print("  UP/DOWN    - Select")
    print("  LEFT/RIGHT - Change")
    print("  ENTER      - Start Workout")
    print("  Q          - Quit")
    print()

    running = True

    # ========================================
    # MAIN LOOP
    # ========================================

    while running:

        success, frame = trainer.camera.read()

        if not success:

            print(
                "Could not read camera frame"
            )

            break

        # ====================================
        # PROCESS FRAME
        # ====================================

        frame = trainer.process_frame(
            frame
        )

        # ====================================
        # SHOW FRAME
        # ====================================

        cv2.imshow(
            "AI Gym Trainer",
            frame
        )

        # ====================================
        # KEYBOARD
        # ====================================

        key = cv2.waitKey(1)

        # ------------------------------------
        # IMPORTANT:
        # Convert OpenCV key to normal value
        # ------------------------------------

        if key == -1:
            continue

        key = key & 0xFF

        # ====================================
        # SETTINGS MODE
        # ====================================

        if trainer.show_settings:

            # ENTER
            if key == 13:

                print()
                print(
                    "Starting workout..."
                )

                config = (
                    trainer.settings_ui
                    .get_config()
                )

                print(
                    f"Exercise: "
                    f"{config['exercise']}"
                )

                print(
                    f"Reps: "
                    f"{config['target_reps']}"
                )

                print(
                    f"Sets: "
                    f"{config['target_sets']}"
                )

                print(
                    f"Rest: "
                    f"{config['rest_seconds']} sec"
                )

                print(
                    f"Weight: "
                    f"{config['weight_kg']} kg"
                )

                trainer.configure_workout(
                    **config
                )

                trainer.show_settings = False

                trainer.start_workout()

                print(
                    "Workout started!"
                )

                continue

            # Q
            if key == ord("q"):

                running = False

                continue

            # Other settings keys
            trainer.settings_ui.handle_key(
                key
            )

            continue

        # ====================================
        # DASHBOARD MODE
        # ====================================

        if trainer.show_dashboard:

            # D = return to workout
            if key == ord("d"):

                trainer.toggle_dashboard()

            # Q = quit
            elif key == ord("q"):

                running = False

            continue

        # ====================================
        # WORKOUT MODE
        # ====================================

        # ------------------------------------
        # W = start workout
        # ------------------------------------

        if key == ord("w"):

            if not trainer.workout.is_active():

                trainer.start_workout()

        # ------------------------------------
        # S = manually complete set
        # ------------------------------------

        elif key == ord("s"):

            trainer.complete_set()

        # ------------------------------------
        # R = reset
        # ------------------------------------

        elif key == ord("r"):

            trainer.reset()

        # ------------------------------------
        # D = dashboard
        # ------------------------------------

        elif key == ord("d"):

            trainer.toggle_dashboard()

        # ------------------------------------
        # Q = quit
        # ------------------------------------

        elif key == ord("q"):

            running = False

    # ========================================
    # SAVE WORKOUT
    # ========================================

    try:

        summary = trainer.get_summary()

        if summary["completed"]:

            workout_id = (
                trainer.save_workout()
            )

            print()
            print(
                "================================"
            )

            print(
                "WORKOUT SAVED"
            )

            print(
                f"Workout ID: {workout_id}"
            )

            print(
                f"Total Reps: "
                f"{summary['total_reps']}"
            )

            print(
                f"Total Sets: "
                f"{summary['total_sets']}"
            )

            print(
                f"Form Score: "
                f"{summary['average_form_score']}%"
            )

            print(
                f"Duration: "
                f"{summary['duration']}"
            )

            print(
                f"Calories: "
                f"{summary['calories_burned']} kcal"
            )

            print(
                "================================"
            )

    except Exception as error:

        print(
            f"Could not save workout: {error}"
        )

    # ========================================
    # CLEANUP
    # ========================================

    trainer.stop()

    cv2.destroyAllWindows()

    print()
    print(
        "AI Gym Trainer stopped."
    )


if __name__ == "__main__":

    main()

