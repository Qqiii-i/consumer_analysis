
import pandas as pd


def calculate_monthly_trend(data):
    """
    统计每个月的消费支出。
    """
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
        expense_data["transaction_date"]
        .dt.to_period("M")
        .astype(str)
    )

    result = (
        expense_data.groupby("month")["amount"]
        .sum()
        .reset_index()
    )

    result.columns = ["month", "total_expense"]

    return result.sort_values("month").reset_index(drop=True)

def calculate_moving_average(data, window=2):
    """
    计算月度消费支出的移动平均值。
    """
    if window <= 0:
        raise ValueError("移动平均窗口必须大于0")

    result = data.copy()

    result["moving_average"] = (
        result["total_expense"]
        .rolling(window=window)
        .mean()
    )

    return result

def predict_next_month_expense(data):
    """
    使用最近3个月的消费金额预测下个月支出。
    """
    if len(data) < 3:
        raise ValueError("至少需要3个月的消费数据才能进行预测")

    recent_expenses = data["total_expense"].tail(3)

    prediction = recent_expenses.mean()

    return round(prediction, 2)

def calculate_expense_by_period(data, period="D"):
    """
    按指定时间周期统计消费支出。
    D：日统计
    W：周统计
    M：月统计
    Y：年统计
    """
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

    expense_data["period"] = (
        expense_data["transaction_date"]
        .dt.to_period(period)
        .astype(str)
    )

    result = (
        expense_data.groupby("period")["amount"]
        .sum()
        .reset_index()
    )

    result.columns = ["period", "total_expense"]

    return result.sort_values("period").reset_index(drop=True)

def calculate_expense_frequency(data, period="M"):
    """
    按指定时间周期统计消费次数。
    D：日统计
    W：周统计
    M：月统计
    Y：年统计
    """
    expense_data = data[
        data["transaction_type"] == "支出"
    ].copy()

    expense_data["transaction_date"] = pd.to_datetime(
        expense_data["transaction_date"],
        errors="coerce"
    )

    expense_data = expense_data.dropna(
        subset=["transaction_date"]
    )

    expense_data["period"] = (
        expense_data["transaction_date"]
        .dt.to_period(period)
        .astype(str)
    )

    result = (
        expense_data.groupby("period")
        .size()
        .reset_index(name="transaction_count")
    )

    return result.sort_values("period").reset_index(drop=True)

def calculate_expense_distribution(data, period="M"):
    """
    按日、周、月、年统计不同金额区间的消费笔数
    """
    expense_data = data[
        data["transaction_type"] == "支出"
    ].copy()

    expense_data["transaction_date"] = pd.to_datetime(
        expense_data["transaction_date"]
    )

    expense_data["period"] = (
        expense_data["transaction_date"].dt.to_period(period).astype(str)
    )

    bins = [0, 50, 100, 500, float("inf")]
    labels = ["0-50元", "50-100元", "100-500元", "500元以上"]

    expense_data["amount_range"] = pd.cut(
        expense_data["amount"],
        bins=bins,
        labels=labels,
        right=False
    )

    result = (
        expense_data.groupby(
            ["period", "amount_range"],
            observed=False
        )
        .size()
        .reset_index(name="transaction_count")
    )

    return result