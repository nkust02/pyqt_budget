from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime, date  # ✅ 新增匯入

# ✅ 加入：Matplotlib 中文字型設定（用 Windows 內建）
import matplotlib
from matplotlib import font_manager

# 依序嘗試可用字型（微軟正黑體/微軟雅黑/Arial Unicode）
font_candidates = ["Microsoft JhengHei", "Microsoft YaHei", "Arial Unicode MS"]
for fam in font_candidates:
    try:
        path = font_manager.findfont(fam, fallback_to_default=False)
        if path:
            matplotlib.rcParams["font.family"] = fam
            matplotlib.rcParams["axes.unicode_minus"] = False
            break
    except Exception:
        pass
# 若以上都沒有，Matplotlib 仍會用預設字型，但中文可能是方塊

class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.figure = Figure(figsize=(8, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.ax = None
    
    def plot(self, x, y, marker=None):
        """繪製折線圖"""
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.ax.plot(x, y, marker=marker, linestyle='-', linewidth=2, markersize=8, color='blue')
        
        if x and len(x) > 0:
            self.ax.set_xticks(x)
            # ✅ 同時支援 date/datetime
            date_labels = [d.strftime('%m-%d') if isinstance(d, (datetime, date)) else str(d) for d in x]
            self.ax.set_xticklabels(date_labels, rotation=45, ha='right')
        
        self.ax.grid(True, alpha=0.3)
        
        # ✅ 增加 top 邊距，防止標題被擋
        self.figure.tight_layout()
        self.figure.subplots_adjust(top=0.92)  # 留 8% 空間給標題
        self.canvas.draw()
    
    def set_xlabel(self, label: str):
        """設定 X 軸標籤"""
        if self.ax is not None:
            self.ax.set_xlabel(label, fontsize=11, fontproperties='Microsoft YaHei')
            self.canvas.draw()

    def set_ylabel(self, label: str):
        """設定 Y 軸標籤"""
        if self.ax is not None:
            self.ax.set_ylabel(label, fontsize=11, fontproperties='Microsoft YaHei')
            self.canvas.draw()

    def set_title(self, title: str):
        """設定圖表標題"""
        if self.ax is not None:
            self.ax.set_title(title, fontsize=12, fontweight='bold', fontproperties='Microsoft YaHei')
            self.canvas.draw()
    
    def clear(self):
        """清空圖表"""
        self.figure.clear()
        self.ax = None
        self.canvas.draw()