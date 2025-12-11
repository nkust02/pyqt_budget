from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Dict, Optional
from collections import defaultdict

@dataclass
class BudgetItem:
    kind: str        # ✅ 新增：收入或支出
    name: str
    category: str
    amount: float
    when: date

class BudgetData:
    def __init__(self):
        self.items: List[BudgetItem] = []
    
    def add_item(self, kind: str, name: str, category: str, amount: float, when: date):
        item = BudgetItem(kind=kind, name=name, category=category, amount=amount, when=when)
        self.items.append(item)
    
    def timeseries(self):
        """回傳 (日期列表, 累積淨值列表) - 同一天資料合併"""
        if not self.items:
            return [], []
        
        # 按日期分組，同一天的資料加總
        daily_data = {}
        for item in self.items:
            if item.when not in daily_data:
                daily_data[item.when] = 0.0
            
            if item.kind == '收入':
                daily_data[item.when] += item.amount
            else:
                daily_data[item.when] -= item.amount
        
        # 按日期排序
        sorted_dates = sorted(daily_data.keys())
        
        # 計算累積淨值
        dates = []
        cumulative = []
        balance = 0.0
        for d in sorted_dates:
            dates.append(d)
            balance += daily_data[d]
            cumulative.append(balance)
        
        return dates, cumulative


    def summary(self) -> Dict[str, float]:
        total_income = sum(i.amount for i in self.items if i.kind == '收入')
        total_expense = sum(e.amount for e in self.items if e.kind == '支出')
        net = total_income - total_expense
        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'net': net
        }


    def monthly_summary(self) -> Dict[str, Dict[str, float]]:
        """回傳 dict: { 'YYYY-MM': {'income': x, 'expense': y, 'net': z}, ... }"""
        per_month_income = defaultdict(float)
        per_month_expense = defaultdict(float)
        for item in self.items:
            key = item.when.strftime("%Y-%m")
            if item.kind == '收入':
                per_month_income[key] += item.amount
            else:
                per_month_expense[key] += item.amount
        months = sorted(set(per_month_income.keys()) | set(per_month_expense.keys()))
        result = {}
        for m in months:
            inc = per_month_income.get(m, 0.0)
            exp = per_month_expense.get(m, 0.0)
            result[m] = {'income': inc, 'expense': exp, 'net': inc - exp}
        return result