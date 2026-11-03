from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QComboBox,
    QLineEdit,
    QGroupBox,
    QHBoxLayout,
    QVBoxLayout
)
from esp_controller import ESPController
from protocol import create_packet

class MainWindow(QWidget):

    # ------------------------------------

    def __init__(self):

        super().__init__()
        self.esp = ESPController()

        self.setWindowTitle("Управление ESP32")
        self.resize(600, 400)

        self.label = QLabel("Команда:", self)
        self.label.move(20, 20)

        self.button = QPushButton("Сформировать пакет", self)
        self.button.move(20, 50)
        self.button.clicked.connect(self.button_clicked)

        self.command_box = QComboBox(self)
        self.command_box.addItem("Включить LED", 0x01)
        self.command_box.addItem("Выключить LED", 0x02)
        self.command_box.addItem("Мигнуть LED", 0x03)
        self.command_box.move(100, 17)

        self.data_fields = []

        field_names = [
            "Время включения",
            "Время выключения",
            "Количество миганий",
            "Резерв 1",
            "Резерв 2"
        ]

        container = QWidget(self)
        container.setGeometry(20, 85, 560, 100)

        main_layout = QHBoxLayout(container)
        main_layout.setContentsMargins(0, 0, 0, 0)

        for name in field_names:
            group = QGroupBox(name)

            layout = QVBoxLayout(group)

            field = QLineEdit()
            field.setMaxLength(3)
            field.setPlaceholderText("0–255")

            layout.addWidget(field)
            main_layout.addWidget(group)

            self.data_fields.append(field)

        self.packet_label = QLabel("Пакет ---", self)
        self.packet_label.move(20, 200)
        self.packet_label.resize(400, 30)

        self.command_box.currentIndexChanged.connect(
        self.update_fields_visibility
        )

        self.update_fields_visibility()

    # ------------------------------------

    def update_fields_visibility(self):
        is_blink = self.command_box.currentData() == 0x03

        for i in range(5):
            self.data_fields[i].parentWidget().setVisible(is_blink)

    # ------------------------------------

    def button_clicked(self):
        command = self.command_box.currentData()

        data = []

        for field in self.data_fields:
            text = field.text().strip()

            if text == "":
                value = 0
            else:
                try:
                    value = int(text)
                except ValueError:
                    print("Ошибка: введите целое число")
                    return

                if value < 0 or value > 255:
                    print("Ошибка: значение должно быть от 0 до 255")
                    return

            data.append(value)

        packet = create_packet(command, data)

        self.packet_label.setText(
            "Пакет: " + packet.hex(" ").upper()
        )

        response = self.esp.send_command(command, data)

        print("Ответ ESP:", response)

# ------------------------------------

def closeEvent(self, event):
    self.esp.close()
    event.accept()