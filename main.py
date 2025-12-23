import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from ui_main import MainWindow

current_dir = os.path.dirname(os.path.abspath(__file__))
platforms_path = os.path.join(current_dir, 'platforms')
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = platforms_path


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont("Microsoft JhengHei", 10))  # 全域中文字型
    win = MainWindow()
    win.setWindowTitle("個人財務試算器")  # 純文字標題
    win.show()
    sys.exit(app.exec_())