import streamlit as st
import pandas as pd
from pathlib import Path
from processors.wechat_importer import import_wechat_bill
from processors.cleaner import (
    clean_transactions,
    check_data_quality,
    remove_invalid_transactions
)


def show_data_import():

    # 账单数据导入
    st.divider()
    st.subheader("账单数据导入")

    # 下载账单模板
    template_columns = [
        "transaction_id",
        "transaction_date",
        "description",
        "amount",
        "transaction_type",
        "category",
        "payment_method"
    ]

    template_data = pd.DataFrame(columns=template_columns)

    template_csv = template_data.to_csv(
        index=False,
        encoding="utf-8-sig"
    )

    st.download_button(
        label="下载账单填写模板",
        data=template_csv,
        file_name="消费账单模板.csv",
        mime="text/csv"
    )

    uploaded_file = st.file_uploader(
        "请选择消费账单文件（CSV / Excel / JSON）",
        type=["csv", "xlsx", "json"]
    )

    if uploaded_file is not None:
        if uploaded_file.size == 0:
            st.error("上传的账单文件为空，请重新选择文件。")
            st.stop()

        try:
            if uploaded_file.name.startswith("微信支付账单流水文件") and uploaded_file.name.endswith(".xlsx"):
                data = import_wechat_bill(uploaded_file)
                data_source = "微信支付账单"

            elif uploaded_file.name.endswith(".xlsx"):
                data = pd.read_excel(
                    uploaded_file,
                    engine="openpyxl"
                )
                data_source = "用户上传的账单"

            elif uploaded_file.name.endswith(".json"):
                data = pd.read_json(uploaded_file)
                data_source = "用户上传的账单"


            else:
                data = pd.read_csv(
                    uploaded_file,
                    encoding="utf-8-sig"
                )
                data_source = "用户上传的账单"


            required_columns = [
                "transaction_id",
                "transaction_date",
                "description",
                "amount",
                "transaction_type",
                "category",
                "payment_method"
            ]

            missing_columns = [
                column for column in required_columns
                if column not in data.columns
            ]

            if data.empty:
                st.error("账单文件中没有交易记录，请上传包含实际消费数据的文件。")
                st.stop()

            if missing_columns:
                st.error(
                    f"账单缺少必要字段：{', '.join(missing_columns)}"
                )
                st.stop()

        except Exception as e:
            st.error(f"读取账单失败：{e}")
            st.stop()

    else:
        data_path = Path("data/sample/transactions.csv")

        if data_path.exists():
            data = pd.read_csv(
                data_path,
                encoding="utf-8-sig"
            )
            data_source = "系统模拟账单"
        else:
            st.error("未找到账单文件，请上传 CSV 文件")
            st.stop()

    # 数据清洗
    original_count = len(data)

    # 清洗前检查异常日期和金额
    invalid_dates = pd.to_datetime(
        data["transaction_date"],
        errors="coerce"
    ).isna().sum()

    invalid_amounts = pd.to_numeric(
        data["amount"],
        errors="coerce"
    ).isna().sum()

    data = clean_transactions(data)
    data = remove_invalid_transactions(data)

    cleaned_count = len(data)

    if data.empty:
        st.warning("当前账单没有有效交易记录，请上传包含交易数据的账单。")
        st.stop()

    st.write(f"数据清洗前：{original_count} 条")
    st.write(f"数据清洗后：{cleaned_count} 条")
    st.write(f"清理无效记录：{original_count - cleaned_count} 条")
    st.write(f"清洗前异常日期：{invalid_dates} 条")
    st.write(f"清洗前异常金额：{invalid_amounts} 条")

    # 数据质量检查
    quality_report = check_data_quality(data)

    st.subheader("数据质量检查")
    st.write("各字段缺失值统计")

    missing_data = quality_report["missing_values"].reset_index()
    missing_data.columns = ["字段名称", "缺失数量"]

    st.dataframe(missing_data, width="stretch")

    st.write(
        f"重复交易编号：{quality_report['duplicate_ids']} 条"
    )

    st.write(
        f"无效日期：{quality_report['invalid_dates']} 条"
    )

    st.write(
        f"无效金额：{quality_report['invalid_amounts']} 条"
    )

    st.write(f"当前数据来源：{data_source}")
    st.write(f"当前共有 {len(data)} 条交易记录")
    st.dataframe(data, width="stretch")

    st.session_state["transaction_data"] = data.copy()

    return data