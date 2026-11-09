
MAIN_STYLE = """
QWidget {
    background-color: #080808;
    color: #FFFFFF;
    font-family: Consolas;
    font-size: 13px;
}

QLabel {
    color: #FFFFFF;
    background: transparent;
}

QPushButton {
    background-color: #FFFFFF;
    color: #080808;
    border: 1px solid #FFFFFF;
    padding: 10px 16px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #CCCCCC;
}

QPushButton:pressed {
    background-color: #888888;
}

QLineEdit, QComboBox, QPlainTextEdit {
    background-color: #191919;
    color: #FFFFFF;
    border: 1px solid #444444;
    padding: 8px;
    selection-background-color: #FFFFFF;
    selection-color: #000000;
}

QGroupBox {
    background-color: #111111;
    border: 1px solid #333333;
    margin-top: 14px;
    padding: 12px;
    font-weight: bold;
}

QGroupBox::title {
    color: #AAAAAA;
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 6px;
}

QComboBox QAbstractItemView {
    background-color: #191919;
    color: #FFFFFF;
    selection-background-color: #444444;
}

QPlainTextEdit {
    background-color: #080808;
    color: #CCCCCC;
    border: 1px solid #333333;
    padding: 8px;
    font-family: Consolas;
}

QGroupBox {
    color: #FFFFFF;
}
"""