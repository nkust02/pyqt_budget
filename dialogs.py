from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QMessageBox


class MessageDialog(QDialog):
    """一般訊息對話窗"""
    def __init__(self, title, message):
        super().__init__()
        self.setWindowTitle(title)
        layout = QVBoxLayout()
        layout.addWidget(QLabel(message))
        btn = QPushButton("確定")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)
        self.setLayout(layout)


class ErrorDialog(QDialog):
    """錯誤訊息對話窗"""
    def __init__(self, title, error_msg):
        super().__init__()
        self.setWindowTitle(f"❌ {title}")
        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"錯誤：{error_msg}"))
        btn = QPushButton("關閉")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)
        self.setLayout(layout)


class ConfirmDialog(QDialog):
    """確認對話窗（Yes/No）"""
    def __init__(self, title, message):
        super().__init__()
        self.setWindowTitle(f"❓ {title}")
        self.result = False
        layout = QVBoxLayout()
        layout.addWidget(QLabel(message))
        
        yes_btn = QPushButton("是")
        yes_btn.clicked.connect(lambda: self._set_result(True))
        no_btn = QPushButton("否")
        no_btn.clicked.connect(lambda: self._set_result(False))
        
        layout.addWidget(yes_btn)
        layout.addWidget(no_btn)
        self.setLayout(layout)
    
    def _set_result(self, value):
        self.result = value
        self.accept()