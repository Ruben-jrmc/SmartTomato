import sys
import signal
from src.camera import Camera
from src.model import Model
from src.server import Server
from src.stm_interface import STM_Interface
from src.journal import Journal
import src.signals as sigs
import threading
import time


class Main():
    def __init__(self):
        self.UPLOAD_DIR = "uploads/"
        # self.cam = Camera(self.UPLOAD_DIR)
        # self.stm = STM_Interface("/dev/ttyACM0")
        self.journal = Journal()

        self.server = Server()
        self.server_thread = threading.Thread(
            target=self.server.start, daemon=True)
        self.server_thread.start()

        self.model = Model()

    def mainLoop(self):
        while True:
            continue
            self.listenToSignal(sigs.RX_PREDICT)
            input = self.cam.takeAndSavePhoto()
            output = self.makePrediction(input)
            if output != -1:
                threshold_inc = self.server.get_threshold()
                category = self.classifyModelOutput(output, threshold_inc)
                self.server.update_parameters(last_pred_class=category)
                self.stm.sendSignal(category)

                self.listenToSignal(sigs.RX_TOMATO_OUT)
                print("Tomate sale")

                self.journal.addByCategory(category)
            else:
                self.stm.sendSignal(sigs.TX_UNK)
                self.listenToSignal(sigs.RX_TOMATO_OUT)

    def listenToSignal(self, SIGNAL):
        while self.stm.waitForTrigger() != SIGNAL:
            pass

    def makePrediction(self, img_url) -> int:
        class_ids = self.model.predict(img_url)
        if class_ids.size > 0:
            return class_ids[0]
        return -1

    def classifyModelOutput(self, output, threshold_inc) -> int:
        if output < 0:
            return -1
        approved = (output == 0 or
                    output == 1 or
                    (output == 3 and threshold_inc) or
                    (output == 4 and threshold_inc))
        if approved:
            return sigs.TX_APPROVED
        else:
            return sigs.TX_REJECT


def handlerExit(sig, frame):
    print("Adios :D")
    sys.exit(0)


signal.signal(signal.SIGINT, handlerExit)

main = Main()
main.mainLoop()
