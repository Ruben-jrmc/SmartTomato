import cv2
import time
import threading


class Camera:
    def __init__(self, save_dir="uploads/"):
        self.output_path = save_dir+"photo.jpg"
        self.connect()
        self.latest_frame = None

    def connect(self):
        for i in range(5):
            self.cam = cv2.VideoCapture(i)
            if self.cam.isOpened():
                self.index_cam = i
                break
        threading.Thread(target=self.thread_video, daemon=True).start()
        print("Conexion establecida")

    def takeAndSavePhoto(self) -> str:
        for _ in range(10):
            self.cam.read()
        ret, frame = self.cam.read()
        if ret:
            cv2.imwrite(self.output_path, frame)
        else:
            self.connect()
            return self.takeAndSavePhoto()
        return self.output_path

    def thread_video(self):
        while True:
            success, frame = self.cam.read()
            if not success:
                self.connect()
            ret, buffer = cv2.imencode(".jpg", frame)
            if not ret:
                continue
            self.latest_frame = buffer.tobytes()
            time.sleep(0.1)

    def generate_frames(self):
        while True:
            if self.latest_frame is not None:
                yield (b"--frame\r\n"
                       b"Content-Type: image/jpeg\r\n\r\n" + self.latest_frame + b"\r\n")
            time.sleep(0.03)

    def __del__(self):
        self.cam.release()
