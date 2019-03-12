# from PyQt5.QtCore import
import sys
from PyQt5.QtWidgets import QApplication, QInputDialog, QWidget, QPushButton, QLineEdit, QFormLayout
from PyQt5.QtCore import QRect


class IntInputTestWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Input liczbowy'
        self.geom = QRect(100, 100, 640, 480)
        self.getInputBtn = None
        self.getInputRes = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.geom)

        fl = QFormLayout()
        get_input_btn = self.getInputBtn = QPushButton('Pobierz liczbę')
        get_input_btn.clicked.connect(self.get_input_clicked)
        get_input_res = self.getInputRes = QLineEdit()
        get_input_res.setEnabled(False)
        fl.addRow(get_input_btn, get_input_res)

        self.setLayout(fl)
        self.adjustSize()
        self.show()

    def get_input_clicked(self):
        number, result = QInputDialog.getInt(self, 'Give number', 'Enter some integer')
        self.getInputRes.setText(str(number) if result else '')


def get_input_integer():
    app = QApplication(sys.argv)
    ex = IntInputTestWidget()
    return app.exec_()


if __name__ == '__main__':
    get_input_integer()
