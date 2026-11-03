import serial
import time
from protocol import create_packet

class ESPController:

    def __init__(self, port="COM5", baudrate=9600):
        self.esp = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)
        self.esp.reset_input_buffer()

    def send_command(self, command, data=None):

        if data is None:
            data = [0, 0, 0, 0, 0]

        packet = create_packet(command, data)

        print("Отправляем:", packet.hex(" ").upper())

        self.esp.write(packet)

        response = self.esp.readline().decode(
            "utf-8", errors="ignore"
        ).strip()

        return response

    def close(self):
        if self.esp.is_open:
            self.esp.close()