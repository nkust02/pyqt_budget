from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QDateEdit, QMessageBox, QListWidget, QListWidgetItem,
    QScrollArea  # ✅ 新增
)
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QColor
from plot_widget import PlotWidget
from dialogs import MessageDialog
from logic import BudgetData
from factories import DialogFactory


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('個人財務試算器')
        self.data = BudgetData()  # 確保有初始化
        self._build_ui()


    def _build_ui(self):
        main_layout = QVBoxLayout()

        # ✅ 用 QScrollArea 包裝輸入列
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Input row
        row = QHBoxLayout()
        self.kind_cb = QComboBox()
        self.kind_cb.addItems(['收入', '支出'])
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText('項目名稱')
        self.cat_edit = QLineEdit()
        self.cat_edit.setPlaceholderText('類別')
        self.amount_edit = QLineEdit()
        self.amount_edit.setPlaceholderText('金額')
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())  # 預設今天
        self.add_btn = QPushButton('新增')
        self.add_btn.clicked.connect(self.add_item)


        row.addWidget(self.kind_cb)
        row.addWidget(self.name_edit)
        row.addWidget(self.cat_edit)
        row.addWidget(self.amount_edit)
        row.addWidget(self.date_edit)
        row.addWidget(self.add_btn)
        
        scroll_layout.addLayout(row)
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        scroll.setMaximumHeight(80)  # ✅ 限制高度
        main_layout.addWidget(scroll)


        # List and controls
        mid = QHBoxLayout()
        
        # 左側：清單 + 刪除按鈕
        left_col = QVBoxLayout()
        self.list_widget = QListWidget()
        left_col.addWidget(self.list_widget)
        
        # ✅ 加入刪除按鈕
        self.delete_btn = QPushButton('刪除選中項目')
        self.delete_btn.clicked.connect(self.delete_selected_item)
        left_col.addWidget(self.delete_btn)
        
        mid.addLayout(left_col)

        right_col = QVBoxLayout()
        self.calculate_btn = QPushButton('計算')
        self.calculate_btn.clicked.connect(self.calculate)
        self.summary_label = QLabel('總收入: 0 | 總支出: 0 | 淨值: 0')
        right_col.addWidget(self.calculate_btn)
        right_col.addWidget(self.summary_label)

        # 新增：每月統計清單（顯示在右側）
        from PyQt5.QtWidgets import QListWidget as _QListWidget  # 保留型別
        self.monthly_list = _QListWidget()
        self.monthly_list.setFixedWidth(320)  # 可調整寬度
        right_col.addWidget(self.monthly_list)

        mid.addLayout(right_col)
        main_layout.addLayout(mid)


        # Plot
        self.plot = PlotWidget()
        main_layout.addWidget(self.plot, 1)  # stretch=1 讓圖表佔據更多空間


        self.setLayout(main_layout)


    def add_item(self):
        # 取得輸入
        name = self.name_edit.text().strip()
        category = self.cat_edit.text().strip()
        amount_text = self.amount_edit.text().strip()
        kind = self.kind_cb.currentText()
        when = self.date_edit.date().toPyDate()

        # ✅ 先檢查項目名稱
        if not name:
            DialogFactory.create_error("輸入錯誤", "項目名稱不可為空").exec_()
            return

        # ✅ 再檢查金額
        if not amount_text:
            DialogFactory.create_error("輸入錯誤", "金額需輸入值").exec_()
            return

        try:
            amount = float(amount_text)
            if amount < 0:
                DialogFactory.create_error("輸入錯誤", "金額不可為負數").exec_()
                return
        except ValueError:
            DialogFactory.create_error("輸入錯誤", "金額必須為數字").exec_()
            return

        # 新增資料
        try:
            self.data.add_item(kind, name, category, amount, when)
            DialogFactory.create_message("成功", "資料已新增").exec_()
            self.refresh_list()
            self.update_chart()
            # 清空輸入
            self.name_edit.clear()
            self.cat_edit.clear()
            self.amount_edit.clear()
            self.date_edit.setDate(QDate.currentDate())
        except Exception as e:
            DialogFactory.create_error("新增失敗", str(e)).exec_()


    def calculate(self):
        """按計算按鈕時更新圖表與統計"""
        try:
            summ = self.data.summary()
            self.summary_label.setText(
                f"總收入: {summ['total_income']:.2f} | 總支出: {summ['total_expense']:.2f} | 淨值: {summ['net']:.2f}"
            )
            
            # 更新圖表（調用 update_chart）
            self.update_chart()
            
            # 更新每月統計
            self.monthly_list.clear()
            monthly = self.data.monthly_summary()
            for m in sorted(monthly.keys()):
                v = monthly[m]
                text = f"{m}  收入: {v['income']:.2f}  支出: {v['expense']:.2f}  淨值: {v['net']:.2f}"
                item = QListWidgetItem(text)
                self.monthly_list.addItem(item)
        except Exception as e:
            MessageDialog('計算錯誤', str(e), self).exec_()

    def delete_item(self, row):
        """刪除指定列（row）的項目"""
        try:
            # 先確認再刪除
            dialog = DialogFactory.create_confirm("刪除確認", "確定要刪除這筆記錄？")
            dialog.exec_()
            if dialog.result:
                # ✅ 直接用索引刪除，不解析文字
                if 0 <= row < len(self.data.items):
                    del self.data.items[row]
                    self.list_widget.takeItem(row)
                    DialogFactory.create_message("成功", "資料已刪除").exec_()
                    self.refresh_list()  # 重新整理清單
                    self.update_chart()  # 更新圖表
                else:
                    DialogFactory.create_error("錯誤", "無效的項目索引").exec_()
        except Exception as e:
            DialogFactory.create_error("刪除失敗", str(e)).exec_()

    def delete_selected_item(self):
        """刪除當前選中的項目"""
        current_row = self.list_widget.currentRow()
        if current_row >= 0:
            self.delete_item(current_row)
        else:
            DialogFactory.create_error("錯誤", "請先選擇要刪除的項目").exec_()

    def refresh_list(self):
        """重新載入清單顯示所有項目"""
        self.list_widget.clear()
        
        # 按日期倒序排列（最新在上）
        sorted_items = sorted(self.data.items, key=lambda x: x.when, reverse=True)
        
        for item in sorted_items:
            text = f"{item.kind}: {item.name} ({item.category}) - ${item.amount:.2f} - {item.when}"
            list_item = QListWidgetItem(text)
            
            # 收入綠色，支出紅色
            if item.kind == '收入':
                from PyQt5.QtGui import QColor
                list_item.setForeground(QColor('green'))
            else:
                from PyQt5.QtGui import QColor
                list_item.setForeground(QColor('red'))
            
            self.list_widget.addItem(list_item)
    
    def update_chart(self):
        """新增資料後立即更新圖表"""
        try:
            dates, balances = self.data.timeseries()
            if dates and balances:
                self.plot.plot(dates, balances, marker='o')
                self.plot.set_xlabel('日期')
                self.plot.set_ylabel('累積淨值（元）')
                self.plot.set_title('財務趨勢圖')
        except Exception as e:
            print(f"更新圖表錯誤: {e}")