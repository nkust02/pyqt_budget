# PyQt5 個人財務試算器 — 人機介面期末專題

## 📋 專案說明
使用 PyQt5 設計圖形介面的個人財務管理系統，支援收入/支出紀錄、計算與圖表可視化。

## 🏗️ 程式架構

### 副程式（模組）
1. **ui_main.py**：主視窗 UI（QLineEdit、QPushButton、QComboBox、MatplotlibWidget）
2. **dialogs.py**：自訂對話窗（QDialog，錯誤訊息或確認視窗）
3. **其他模組**：資料處理、計算邏輯等

### 主程式
- **main.py**：應用啟動進入點（含 `if __name__ == '__main__'`）

## 🚀 執行方式

### 環境準備


# 安裝依賴
pip install -r requirements.txt


### 啟動應用

python main.py


## 🧪 測試方式

### 基本功能測試
1. **選擇收入/支出**：在 QLineEdit 輸入金額、類別、日期
2. **新增記錄**：按下「新增」按鈕，資料加入表內
3. **計算結果**：按下「計算」按鈕，顯示總收入、總支出、淨值
4. **圖表更新**：Matplotlib 折線圖自動更新
5. **錯誤訊息**：輸入無效資料時，QDialog 顯示錯誤提示

## 📊 主要元件

| 元件 | 用途 |
|------|------|
| QLineEdit | 輸入金額、類別、備註 |
| QPushButton | 新增、計算、刪除、清空等操作 |
| QComboBox | 選擇類別（食物、交通、娛樂等） |
| QTableWidget | 顯示記錄列表 |
| MatplotlibWidget | 折線圖（趨勢分析） |
| QDialog | 錯誤訊息、確認視窗 |

## 📁 專案結構
```
pyqt_budget/
├── main.py              # 應用啟動進入點
├── ui_main.py           # 主視窗 UI 設計
├── dialogs.py           # 自訂對話窗
├── plot_widget.py       # Matplotlib 圖表元件
├── logic.py             # 資料與邏輯處理
├── factories.py         # 工廠模式
├── requirements.txt     # 依賴清單
├── README.md            # 本檔案

```

## 🔧 技術棧
- **GUI 框架**：PyQt5
- **圖表繪製**：Matplotlib
- **資料處理**：NumPy
- **語言**：Python 3.8+

## 📝 功能說明

### 資料管理
- 使用 `BudgetItem` dataclass 儲存每筆記錄（kind、name、category、amount、when）
- `BudgetData` 類別管理所有收支資料
- 支援同一天多筆資料自動加總

### 計算與分析
- 計算總收入、總支出、淨值
- 按月份統計
- Matplotlib 折線圖視覺化

### 錯誤處理
- QDialog 顯示輸入驗證錯誤
- 確認刪除操作視窗