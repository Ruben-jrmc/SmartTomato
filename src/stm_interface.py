import serial
import time
import src.signals as sigs


class STM_Interface:
    def __init__(self,  port):
        self.port = port
        self.ser = serial.Serial(port, baudrate=115200, timeout=1)
        time.sleep(1)
        print("Conexion establecida con stm")

    def toggleBand(self):
        self.sendSignal(sigs.TX_TOGGLE_BAND)

    def waitForTrigger(self):
        print("Esperando por señal")
        while True:
            if self.ser.in_waiting > 0:
                data = self.ser.readline().decode('utf-8').strip()
                break
        print("Señal recibida{%d}", data[0])
        return data[0]

    def sendSignal(self, signal):
        self.ser.write(signal)
