import pandas as pd

def calculate_monthly_trend(data):
    # 统计每个月的消费支出。
    expense_data = data[
        data["transaction_type"] == "支出"
    ].copy()

    expense_data["transaction_date"] = pd.to_datetime(
        expense_data["transaction_date"],
        errors="coerce"
    )

    expense_data["amount"] = pd.to_numeric(
        expense_data["amount"],
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

def calculate_monthly_category_ratio(data):
    # 计算每个月各消费类别的金额及其占当月总消费的比例。
    expense_data = data[
        data["transaction_type"] == "支出"
    ].copy()

    expense_data["transaction_date"] = pd.to_datetime(
        expense_data["transaction_date"],
        errors="coerce"
    )

    expense_data["amount"] = pd.to_numeric(
        expense_data["amount"],
        errors="coerce"
    )

    expense_data = expense_data.dropna(
        subset=["transaction_date", "amount", "category"]
    )

    expense_data = expense_data[
        expense_data["amount"] > 0
    ]

    expense_data["month"] = (
        expense_data["transaction_date"]
        .dt.to_period("M")
        .astype(str)
    )

    # 统计每个月各类别的消费金额
    monthly_category = (
        expense_data.groupby(
            ["month", "category"]
        )["amount"]
        .sum()
        .reset_index()
    )

    # 计算每个月的消费总额
    monthly_total = (
        monthly_category.groupby("month")["amount"]
        .transform("sum")
    )

    # 计算各类别占当月消费的比例
    monthly_category["percentage"] = (
        monthly_category["amount"]
        / monthly_total
        * 100
    )

    return monthly_category

def calculate_moving_average(data, window=2):
    # 计算月度消费支出的移动平均值。
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
    # 使用最近3个月的消费金额预测下个月支出。
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
    # 按日、周、月、年统计不同金额区间的消费笔数
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
    labels = ["CNY 0-50", "CNY 50-100", "CNY 100-500", "Above CNY 500"]

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

def generate_consumption_insights(data):
    # 根据消费记录生成消费偏好与行为特征分析。
    expense_data = data[
        data["transaction_type"] == "支出"
    ].copy()

    expense_data["amount"] = pd.to_numeric(
        expense_data["amount"],
        errors="coerce"
    )

    expense_data["transaction_date"] = pd.to_datetime(
        expense_data["transaction_date"],
        errors="coerce"
    )

    expense_data = expense_data.dropna(
        subset=["amount", "transaction_date", "category"]
    )

    expense_data = expense_data[
        expense_data["amount"] > 0
    ]

    if expense_data.empty:
        return ["暂无有效消费记录，无法进行消费行为分析。"]

    insights = []

    # 基本消费情况
    total_expense = expense_data["amount"].sum()
    transaction_count = len(expense_data)
    average_amount = total_expense / transaction_count

    insights.append(
        f"累计消费 {total_expense:.2f} 元，共 {transaction_count} 笔，"
        f"平均每笔消费 {average_amount:.2f} 元。"
    )

    # 消费金额最高的类别
    category_amount = (
        expense_data.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    main_category = category_amount.index[0]
    main_ratio = category_amount.iloc[0] / total_expense * 100

    insights.append(
        f"消费金额最高的类别为「{main_category}」，"
        f"占总消费的 {main_ratio:.2f}%。"
    )

    # 消费笔数最多的类别
    category_count = (
        expense_data.groupby("category")
        .size()
        .sort_values(ascending=False)
    )

    frequent_category = category_count.index[0]

    insights.append(
        f"交易笔数最多的类别为「{frequent_category}」，"
        f"共消费 {category_count.iloc[0]} 笔。"
    )

    # 消费集中度：前三个消费类别的金额占比
    top3_ratio = (
        category_amount.head(3).sum()
        / total_expense
        * 100
    )

    insights.append(
        f"消费金额排名前三的类别合计占总消费的 "
        f"{top3_ratio:.2f}%，可用于观察消费集中程度。"
    )

    # 消费日期分布
    weekday_names = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }

    weekday_count = (
        expense_data["transaction_date"]
        .dt.dayofweek
        .value_counts()
    )

    busiest_weekday = weekday_names[weekday_count.idxmax()]

    insights.append(
        f"账单记录中消费最频繁的日期为{busiest_weekday}，"
        f"共 {weekday_count.max()} 笔。"
    )

    return insights