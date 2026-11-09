import sys
from ui.styles import MAIN_STYLE
from PySide6.QtWidgets import QApplication, QMessageBox
from serial import SerialException

from window import MainWindow

app = QApplication(sys.argv)
app.setStyleSheet(MAIN_STYLE)

try:
    window = MainWindow()
    window.show()

except SerialException as error:
    QMessageBox.critical(
        None,
        "Ошибка подключения",
        f"Не удалось подключиться к ESP8266\n\n{error}"
    )
    sys.exit(1)

sys.exit(app.exec())