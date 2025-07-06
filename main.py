import sys
from PyQt5.QtWidgets import QApplication
from ui.function_window import FunctionWindow


def main():
    app = QApplication(sys.argv)
    window = FunctionWindow(None)
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()