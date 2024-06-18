import database
import logging
import buzzer
import model
import cv2

DROWSY_CONSECUTIVE_FRAMES = 5
SLEEP_CONSECUTIVE_FRAMES = 10

drowsy_frames_counter = 0

logging.basicConfig(filename="drowsiness_history.log", level=logging.INFO)

def main():
    """Main function to start the drowsiness detection system."""
    database.initialize_tables()

    capture = cv2.VideoCapture(0)
    (ret, frame) = capture.read()

    while ret:

        resized_frame = model.resize_frame(frame)
        face = model.detect_first_face(resized_frame)

        if face is not None:

            face_landmarks = model.get_face_landmarks(resized_frame, face)
            ear_value = model.calculate_average_ear(face_landmarks)
            is_drowsy = model.is_drowsy(ear_value)

            if is_drowsy:
                drowsy_frames_counter += 1

                if drowsy_frames_counter >= SLEEP_CONSECUTIVE_FRAMES:
                    pass

                elif drowsy_frames_counter >= DROWSY_CONSECUTIVE_FRAMES:
                    pass

            else:
                drowsy_frames_counter = 0

            face_with_landmarks = model.draw_landmarks_on_face(resized_frame, face_landmarks)
            cv2.imshow("Face Landmarks", face_with_landmarks)

            print(f"EAR Value: {ear_value}")

        cv2.imshow("Captured Frame", resized_frame)
        (ret, frame) = capture.read()

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


    capture.release()
    cv2.destroyAllWindows()
    buzzer.clean_pins_up()

if __name__ == "__main__":
    main()