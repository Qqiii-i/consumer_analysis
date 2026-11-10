import pandas as pd
import re

def import_wechat_bill(uploaded_file):
    # 读取微信支付 Excel 账单，并转换为项目统一格式。
    # 不把交易单号等字段识别为数字
    raw_data = pd.read_excel(
        uploaded_file,
        header=None,
        dtype=str,
        engine="openpyxl"
    )

    # 自动查找微信账单明细表头
    header_index = None

    for index, row in raw_data.iterrows():
        values = row.fillna("").astype(str).str.strip().tolist()

        if (
            "交易时间" in values
            and "交易类型" in values
            and "交易单号" in values
        ):
            header_index = index
            break

    if header_index is None:
        raise ValueError(
            f"无法识别微信账单表头。文件前15行内容："
            f"{raw_data.head(15).to_string(index=False, header=False)}"
        )
    
    # 提取表头及交易明细
    headers = (
        raw_data.iloc[header_index]
        .fillna("")
        .astype(str)
        .str.strip()
        .tolist()
    )

    data = raw_data.iloc[header_index + 1:].copy()
    data.columns = headers

    # 检查必要字段
    required_columns = [
        "交易时间",
        "交易类型",
        "交易对方",
        "商品",
        "收/支",
        "金额(元)",
        "支付方式",
        "交易单号"
    ]

    missing = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing:
        raise ValueError(
            f"微信账单缺少字段：{', '.join(missing)}"
        )

    # 删除没有交易时间的空白行
    data = data.dropna(subset=["交易时间"])

    data = data[
        data["交易时间"].astype(str).str.strip() != ""
    ].copy()

    # 转换为项目统一字段
    result = pd.DataFrame()

    result["transaction_id"] = (
        data["交易单号"].astype(str).str.strip()
    )

    result["transaction_date"] = pd.to_datetime(
        data["交易时间"],
        errors="coerce"
    )

    result["description"] = (
        data["交易对方"].fillna("").astype(str).str.strip()
        + " "
        + data["商品"].fillna("").astype(str).str.strip()
    ).str.strip()

    # 去除人民币符号和千位分隔符
    amount = (
        data["金额(元)"]
        .fillna("")
        .astype(str)
        .str.replace("¥", "", regex=False)
        .str.replace("￥", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    result["amount"] = pd.to_numeric(
        amount,
        errors="coerce"
    )

    # 根据微信账单的收/支字段识别交易类型
    income_expense = (
        data["收/支"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    result["transaction_type"] = income_expense.map({
        "收入": "收入",
        "支出": "支出",
        "/": "中性交易",
        "": "中性交易"
    }).fillna("中性交易")

    result["category"] = "未分类"

    # 隐藏银行卡号后四位，保留银行名称和卡类型
    result["payment_method"] = (
        data["支付方式"]
        .fillna("未填写")
        .astype(str)
        .str.strip()
        .apply(
            lambda x: re.sub(
                r"\s*[（(]\s*\d{4}\s*[）)]",
                "",
                x
            ).strip()
        )
    )

    return result.reset_index(drop=True)