import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from ui_main import MainWindow
from dialogs import MessageDialog  # 假設 dialogs.py 在相同目錄


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()

    # 在事件迴圈啟動後顯示模態對話窗
    QTimer.singleShot(0, lambda: MessageDialog("標題", "這是一個訊息").exec_())

    sys.exit(app.exec_())