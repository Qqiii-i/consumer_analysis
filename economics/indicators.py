import pandas as pd

def calculate_basic_indicators(data):
    # 计算总收入、总支出和收支结余。
    income = data.loc[
        data["transaction_type"] == "收入", "amount"
    ].sum()

    expense = data.loc[
        data["transaction_type"] == "支出", "amount"
    ].sum()

    balance = income - expense

    return {
        "total_income": income,
        "total_expense": expense,
        "balance": balance
    }

def calculate_category_statistics(data):
    # 统计各消费类别的支出金额和占比。
    expense_data = data[
        data["transaction_type"] == "支出"
    ]

    category_amount = expense_data.groupby("category")["amount"].sum()

    total_expense = category_amount.sum()

    result = category_amount.reset_index()
    result.columns = ["category", "amount"]

    if total_expense > 0:
        result["percentage"] = (
            result["amount"] / total_expense * 100
        )
    else:
        result["percentage"] = 0.0

    return result.sort_values(
        by="amount", ascending=False
    ).reset_index(drop=True)

def calculate_monthly_expenses(data):
    # 按月份统计消费支出。
    expense_data = data[
        data["transaction_type"] == "支出"
    ].copy()

    expense_data["transaction_date"] = pd.to_datetime(
        expense_data["transaction_date"],
        errors="coerce"
    )

    expense_data = expense_data.dropna(
        subset=["transaction_date", "amount"]
    )

    expense_data["month"] = (
        expense_data["transaction_date"].dt.to_period("M").astype(str)
    )

    result = (
        expense_data.groupby("month")["amount"]
        .sum()
        .reset_index()
    )

    result.columns = ["month", "total_expense"]

    return result.sort_values("month").reset_index(drop=True)

def calculate_engel_coefficient(data):
    # 计算恩格尔系数（餐饮支出 / 总消费支出）
    expense_data = data[
        data["transaction_type"] == "支出"
    ]

    total_expense = expense_data["amount"].sum()

    food_expense = expense_data.loc[
        expense_data["category"] == "餐饮", "amount"
    ].sum()

    if total_expense <= 0:
        return 0.0

    return food_expense / total_expense * 100

def calculate_average_propensity_to_consume(data):
    # 计算平均消费倾向(APC)
    income = data.loc[
        data["transaction_type"] == "收入", "amount"
    ].sum()

    expense = data.loc[
        data["transaction_type"] == "支出", "amount"
    ].sum()

    if income <= 0:
        return 0.0

    return expense / income

def calculate_saving_rate(data):
    # 计算储蓄率（收支结余 / 总收入）
    income = data.loc[
        data["transaction_type"] == "收入", "amount"
    ].sum()

    expense = data.loc[
        data["transaction_type"] == "支出", "amount"
    ].sum()

    if income <= 0:
        return 0.0

    return (income - expense) / income

def calculate_marginal_propensity_to_consume(data):
    # 根据相邻月份的收入和消费支出变化计算边际消费倾向。
    monthly_data = data.copy()

    monthly_data["transaction_date"] = pd.to_datetime(
        monthly_data["transaction_date"],
        errors="coerce"
    )

    monthly_data = monthly_data.dropna(
        subset=["transaction_date", "amount"]
    )

    monthly_data["month"] = (
        monthly_data["transaction_date"].dt.to_period("M").astype(str)
    )

    monthly_summary = monthly_data.pivot_table(
        index="month",
        columns="transaction_type",
        values="amount",
        aggfunc="sum",
        fill_value=0
    )

    if "收入" not in monthly_summary.columns:
        return None

    if "支出" not in monthly_summary.columns:
        return None

    monthly_summary = monthly_summary.sort_index()

    if len(monthly_summary) < 2:
        return None

    previous = monthly_summary.iloc[-2]
    current = monthly_summary.iloc[-1]

    delta_income = current["收入"] - previous["收入"]
    delta_expense = current["支出"] - previous["支出"]

    if delta_income == 0:
        return None

    return delta_expense / delta_income