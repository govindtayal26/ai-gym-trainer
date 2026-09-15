import cv2


class Camera:

    def __init__(self, camera_id=0, width=1280, height=720):

        self.camera_id = camera_id

        self.width = width
        self.height = height

        self.cap = None

    def start(self):

        self.cap = cv2.VideoCapture(self.camera_id)

        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera")

        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            self.width
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            self.height
        )

    def read(self):

        if self.cap is None:
            return False, None

        success, frame = self.cap.read()

        if not success:
            return False, None

        # Mirror camera
        frame = cv2.flip(frame, 1)

        return True, frame

    def release(self):

        if self.cap is not None:
            self.cap.release()

        self.cap = None