import pandas as pd

def clean_transactions(data):
    """
    清洗消费记录中的日期和金额数据。

    参数：
        data：原始消费记录 DataFrame

    返回：
        清洗后的 DataFrame
    """
    # 复制数据，避免修改原始数据
    cleaned_data = data.copy()

    # 将交易日期转换为日期类型
    cleaned_data["transaction_date"] = pd.to_datetime(
        cleaned_data["transaction_date"],
        errors="coerce"
    )

    # 将金额转换为数值类型
    cleaned_data["amount"] = pd.to_numeric(
        cleaned_data["amount"],
        errors="coerce"
    )

    return cleaned_data


def check_data_quality(data):
    """
    检查消费记录的数据质量。
    """
    report = {
        # 每个字段的缺失值数量
        "missing_values": data.isnull().sum(),

        # 重复交易编号的数量
        "duplicate_ids": data["transaction_id"].duplicated().sum(),

        # 无效日期的数量
        "invalid_dates": data["transaction_date"].isnull().sum(),

        # 无效金额的数量
        "invalid_amounts": data["amount"].isnull().sum()
    }

    return report


def remove_invalid_transactions(data):
    """
    自动处理无效和重复交易记录。
    """
    cleaned_data = data.copy()

    # 将空字符串也视为缺失值
    cleaned_data = cleaned_data.replace(r"^\s*$", pd.NA, regex=True)

    # 删除交易编号、日期或金额缺失的记录
    cleaned_data = cleaned_data.dropna(
        subset=["transaction_id", "transaction_date", "amount"]
    )

    # 删除重复交易编号，保留第一条
    cleaned_data = cleaned_data.drop_duplicates(
        subset=["transaction_id"],
        keep="first"
    )

    # 补充其他字段的缺失值
    optional_columns = [
        "description",
        "category",
        "payment_method"
    ]

    for column in optional_columns:
        cleaned_data[column] = cleaned_data[column].fillna("未填写")

    # 重置行索引
    cleaned_data = cleaned_data.reset_index(drop=True)

    return cleaned_data
