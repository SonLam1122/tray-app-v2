import sys
from PyQt5.QtWidgets import QApplication
from ui.main_windows import MiniTrayWindow


def main():
    app = QApplication(sys.argv)
    window = MiniTrayWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
    
    
