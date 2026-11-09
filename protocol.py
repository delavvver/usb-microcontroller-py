HEADER = 0xAA
END = 0x55
DATA_LENGTH = 5

CMD_LED_ON = 0x01
CMD_LED_OFF = 0x02
CMD_LED_BLINK = 0x03

CMD_SET_PIN = 0x10
CMD_SET_MODE = 0x20 

MODE_OFF = 0x00
MODE_ON = 0x01
MODE_PWM = 0x02
MODE_BLINK = 0x03


def create_packet(command, data=None):

    if data is None:
        data = [0] * DATA_LENGTH

    if len(data) != DATA_LENGTH:
        raise ValueError("Пакет должен содержать 5 байтов данных")

    if not 0 <= command <= 255:
        raise ValueError("Команда должна быть в диапазоне 0–255")

    for value in data:
        if not 0 <= value <= 255:
            raise ValueError("Данные должны быть в диапазоне 0–255")

    return bytes([
        HEADER,
        command,
        *data,
        END
    ])
