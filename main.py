import sys
import os
from PyQt5.QtWidgets import QApplication
from ui_main import MainWindow

current_dir = os.path.dirname(os.path.abspath(__file__))
platforms_path = os.path.join(current_dir, 'platforms')
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = platforms_path


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())