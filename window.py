
from datetime import datetime
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QComboBox,
    QLineEdit,
    QGroupBox,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QPlainTextEdit
    
)

from esp_controller import ESPController
from protocol import (
    create_packet,
    CMD_SET_PIN,
    CMD_SET_MODE,
    MODE_OFF,
    MODE_ON,
    MODE_PWM,
    MODE_BLINK
)


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.esp = ESPController()

        self.setWindowTitle("ESP CONTROL SYSTEM")
        self.resize(1000, 720)
        self.setMinimumSize(850, 620)

        # Главный layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 16, 20, 16)
        main_layout.setSpacing(12)

        # ------------------------------------
        # HEADER
        # ------------------------------------

        header_layout = QHBoxLayout()

        title = QLabel("ESP CONTROL SYSTEM")
        title.setStyleSheet(
            "font-size: 22px; font-weight: bold; letter-spacing: 2px;"
        )

        version = QLabel("CONTROL MODULE // 01")
        version.setStyleSheet("color: #888888;")

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(version)

        main_layout.addLayout(header_layout)

        # ------------------------------------
        # SYSTEM STATUS
        # ------------------------------------

        status_layout = QGridLayout()
        status_layout.setSpacing(10)

        connection_box = QGroupBox("SYSTEM STATUS")
        connection_layout = QVBoxLayout(connection_box)

        self.connection_label = QLabel("● CONNECTED")
        self.connection_label.setStyleSheet(
            "color: #FFFFFF; font-size: 18px; font-weight: bold;"
        )

        connection_layout.addWidget(self.connection_label)

        channel_box = QGroupBox("ACTIVE CHANNEL")
        channel_layout = QVBoxLayout(channel_box)

        self.channel_label = QLabel("GPIO 4")
        self.channel_label.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )

        channel_layout.addWidget(self.channel_label)

        protocol_box = QGroupBox("SERIAL INTERFACE")
        protocol_layout = QVBoxLayout(protocol_box)

        protocol_label = QLabel("COM5  //  9600 BAUD")
        protocol_label.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )

        protocol_layout.addWidget(protocol_label)

        status_layout.addWidget(connection_box, 0, 0)
        status_layout.addWidget(channel_box, 0, 1)
        status_layout.addWidget(protocol_box, 0, 2)

        main_layout.addLayout(status_layout)

        # ------------------------------------
        # COMMAND CONTROL
        # ------------------------------------


# ------------------------------------
# COMMAND CONTROL
# ------------------------------------

        command_box = QGroupBox("COMMAND CONTROL")
        command_layout = QGridLayout(command_box)

        # Выбор GPIO
        command_layout.addWidget(QLabel("ACTIVE GPIO"), 0, 0)

        self.pin_box = QComboBox()
        self.pin_box.addItem("GPIO 4", 4)
        self.pin_box.addItem("GPIO 5", 5)
        self.pin_box.addItem("GPIO 12", 12)
        self.pin_box.addItem("GPIO 13", 13)
        self.pin_box.addItem("GPIO 14", 14)

        command_layout.addWidget(self.pin_box, 1, 0)

        # Выбор режима
        command_layout.addWidget(QLabel("OPERATING MODE"), 0, 1)

        self.command_box = QComboBox()
        self.command_box.addItem("OFF", MODE_OFF)
        self.command_box.addItem("ON", MODE_ON)
        self.command_box.addItem("PWM", MODE_PWM)
        self.command_box.addItem("BLINK", MODE_BLINK)

        command_layout.addWidget(self.command_box, 1, 1)

        # Параметр режима
        self.parameter_label = QLabel("PARAMETER")
        command_layout.addWidget(self.parameter_label, 0, 2)

        self.parameter_input = QLineEdit()
        self.parameter_input.setPlaceholderText("0 - 255")
        self.parameter_input.setMaxLength(3)
        self.parameter_input.setMinimumHeight(42)
        self.parameter_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        command_layout.addWidget(self.parameter_input, 1, 2)

        # Кнопка отправки
        self.button = QPushButton("EXECUTE COMMAND")
        self.button.setMinimumHeight(42)
        self.button.clicked.connect(self.button_clicked)

        command_layout.addWidget(self.button, 2, 0, 1, 3)

        main_layout.addWidget(command_box)

        # ------------------------------------
        # PACKET INFORMATION
        # ------------------------------------

        packet_box = QGroupBox("PACKET INFORMATION")
        packet_layout = QVBoxLayout(packet_box)

        self.packet_label = QLabel("PACKET: ---")
        self.packet_label.setWordWrap(True)
        self.packet_label.setStyleSheet(
            "font-family: Consolas; font-size: 14px;"
        )

        packet_layout.addWidget(self.packet_label)

        main_layout.addWidget(packet_box)

        # ------------------------------------
        # LOG AND TELEMETRY
        # ------------------------------------

        bottom_layout = QHBoxLayout()

        log_box = QGroupBox("COMMAND LOG")
        log_layout = QVBoxLayout(log_box)

        self.command_log = QPlainTextEdit()
        self.command_log.setReadOnly(True)
        self.command_log.setMaximumHeight(140)

        log_layout.addWidget(self.command_log)

        telemetry_box = QGroupBox("TELEMETRY")
        telemetry_layout = QVBoxLayout(telemetry_box)

        self.telemetry_label = QLabel("WAITING FOR DATA...")
        self.telemetry_label.setWordWrap(True)

        telemetry_layout.addWidget(self.telemetry_label)

        bottom_layout.addWidget(log_box, 2)
        bottom_layout.addWidget(telemetry_box, 1)

        main_layout.addLayout(bottom_layout)

        # ------------------------------------
        # SIGNALS
        # ------------------------------------

        self.command_box.currentIndexChanged.connect(
            self.update_fields_visibility
        )

        self.update_fields_visibility()

        self.add_log("SYSTEM INITIALIZED")
        self.add_log("ESP8266 CONNECTED")

    # ------------------------------------
    # FIELD VISIBILITY
    # ------------------------------------

    def update_fields_visibility(self):

        mode = self.command_box.currentData()

        if mode == MODE_PWM:
            self.parameter_label.setText("BRIGHTNESS (0-255)")
            self.parameter_input.setPlaceholderText("0 - 255")
            self.parameter_input.setEnabled(True)

        elif mode == MODE_BLINK:
            self.parameter_label.setText("FREQUENCY (1-20 Hz)")
            self.parameter_input.setPlaceholderText("1 - 20")
            self.parameter_input.setEnabled(True)

        else:
            self.parameter_label.setText("NO PARAMETER")
            self.parameter_input.clear()
            self.parameter_input.setEnabled(False)

    # ------------------------------------
    # LOG
    # ------------------------------------

    def add_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")

        self.command_log.appendPlainText(
            f"[{timestamp}] {message}"
        )

    # ------------------------------------
    # SEND COMMAND
    # ------------------------------------

       
    def button_clicked(self):

        pin = self.pin_box.currentData()
        mode = self.command_box.currentData()

        parameter = 0

        if mode in (MODE_PWM, MODE_BLINK):
            text = self.parameter_input.text().strip()

            if not text:
                self.add_log("ERROR: PARAMETER REQUIRED")
                return

            try:
                parameter = int(text)
            except ValueError:
                self.add_log("ERROR: INVALID PARAMETER")
                return

            if mode == MODE_PWM and not 0 <= parameter <= 255:
                self.add_log("ERROR: BRIGHTNESS MUST BE 0-255")
                return

            if mode == MODE_BLINK and not 1 <= parameter <= 20:
                self.add_log("ERROR: FREQUENCY MUST BE 1-20 HZ")
                return

        try:
            pin_data = [pin, 0, 0, 0, 0]
            pin_packet = create_packet(CMD_SET_PIN, pin_data)

            self.esp.send_command(CMD_SET_PIN, pin_data)

            mode_data = [mode, parameter, 0, 0, 0]
            mode_packet = create_packet(CMD_SET_MODE, mode_data)

            response = self.esp.send_command(CMD_SET_MODE, mode_data)

            self.packet_label.setText(
                "PIN: " + pin_packet.hex(" ").upper()
                + "\nMODE: " + mode_packet.hex(" ").upper()
            )

            self.channel_label.setText(f"GPIO {pin}")

            self.add_log(f"GPIO {pin} SELECTED")
            self.add_log(f"MODE {mode} SENT")

            if response:
                self.telemetry_label.setText(response)
                self.add_log(f"ESP: {response}")
            else:
                self.telemetry_label.setText("NO RESPONSE RECEIVED")

        except Exception as error:
            self.connection_label.setText("CONNECTION ERROR")
            self.add_log(f"ERROR: {error}")

        
    # ------------------------------------
    # CLOSE
    # ------------------------------------

    def closeEvent(self, event):
        self.esp.close()
        event.accept()
