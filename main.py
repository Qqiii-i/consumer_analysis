from pathlib import Path
from data_loader import load_transactions
from processors.cleaner import (
    clean_transactions,
    remove_invalid_transactions
)
from economics.indicators import calculate_basic_indicators

def main():
    # 获取项目中的模拟账单路径
    file_path = (
        Path(__file__).parent
        / "data"
        / "sample"
        / "transactions.csv"
    )

    # 读取账单
    data = load_transactions(file_path)

    if data is None:
        return

    # 清洗数据
    data = clean_transactions(data)
    data = remove_invalid_transactions(data)

    if data.empty:
        print("没有有效交易记录。")
        return

    # 计算基本经济指标
    indicators = calculate_basic_indicators(data)

    print("智能消费行为分析平台")
    print("-" * 30)
    print(f"有效交易记录：{len(data)} 条")
    print(f"总收入：{indicators['total_income']:.2f} 元")
    print(f"总支出：{indicators['total_expense']:.2f} 元")
    print(f"收支结余：{indicators['balance']:.2f} 元")

if __name__ == "__main__":
    main()