from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt


class MessageDialog(QDialog):
    """一般訊息對話窗"""
    def __init__(self, title, message, parent=None):
        super().__init__(parent)
        # 移除標題列的「?」Help 按鈕
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # 純文字標題（不要 Emoji）
        self.setWindowTitle(str(title))

        layout = QVBoxLayout()
        layout.addWidget(QLabel(str(message)))
        ok_btn = QPushButton("確定")
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn)
        self.setLayout(layout)