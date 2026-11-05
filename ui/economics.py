import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from economics.indicators import (
    calculate_engel_coefficient,
    calculate_average_propensity_to_consume,
    calculate_saving_rate,
    calculate_marginal_propensity_to_consume
)

def load_cpi_data():
    cpi_path = Path("data/cpi/cpi.csv")

    if not cpi_path.exists():
        return None

    cpi_data = pd.read_csv(cpi_path)

    cpi_data["month"] = pd.to_datetime(
        cpi_data["month"],
        format="%Y-%m",
        errors="coerce"
    )

    cpi_data["mom_cpi"] = pd.to_numeric(
        cpi_data["mom_cpi"],
        errors="coerce"
    )

    cpi_data = cpi_data.dropna(
        subset=["month", "mom_cpi"]
    )

    return cpi_data.sort_values("month").reset_index(drop=True)


def calculate_expense_yoy(data):
    """
    计算个人消费支出同比增长率。
    """
    expense_data = data[
        data["transaction_type"] == "支出"
    ].copy()

    expense_data["month"] = (
        pd.to_datetime(
            expense_data["transaction_date"],
            errors="coerce"
        )
        .dt.to_period("M")
    )

    expense_data["amount"] = pd.to_numeric(
        expense_data["amount"],
        errors="coerce"
    )

    expense_data = expense_data.dropna(
        subset=["month", "amount"]
    )

    monthly_expense = (
        expense_data.groupby("month")["amount"]
        .sum()
        .reset_index()
        .sort_values("month")
    )

    monthly_expense["last_year_amount"] = (
        monthly_expense["month"].apply(
            lambda month: monthly_expense.loc[
                monthly_expense["month"] == month - 12,
                "amount"
            ].sum()
            if (monthly_expense["month"] == month - 12).any()
            else None
        )
    )

    monthly_expense["yoy_growth"] = (
        (
            monthly_expense["amount"]
            - monthly_expense["last_year_amount"]
        )
        / monthly_expense["last_year_amount"]
        * 100
    )

    monthly_expense.loc[
        monthly_expense["last_year_amount"] == 0,
        "yoy_growth"
    ] = None

    monthly_expense["month"] = (
        monthly_expense["month"].astype(str)
    )

    return monthly_expense

def show_cpi_analysis(data):
    st.divider()
    st.subheader("CPI 物价指数与个人消费分析")

    cpi_data = load_cpi_data()

    if cpi_data is None or cpi_data.empty:
        st.warning("暂无 CPI 数据，请检查 data/cpi/cpi.csv 文件。")
        return

    expense_data = data[
        data["transaction_type"] == "支出"
    ].copy()

    expense_data["month"] = (
        pd.to_datetime(
            expense_data["transaction_date"],
            errors="coerce"
        )
        .dt.to_period("M")
        .astype(str)
    )

    monthly_expense = (
        expense_data.groupby("month")["amount"]
        .sum()
        .reset_index()
    )

    cpi_data["month"] = cpi_data["month"].dt.strftime("%Y-%m")

    result = pd.merge(
        monthly_expense,
        cpi_data,
        on="month",
        how="inner"
    )

    if result.empty:
        st.info("个人账单与 CPI 数据没有重合月份，暂时无法比较。")
        return

    # 将环比 CPI 转换为以首个月份为 100 的价格指数
    result = result.sort_values("month").reset_index(drop=True)

    result["cpi_index"] = 100.0

    for i in range(1, len(result)):
        result.loc[i, "cpi_index"] = (
            result.loc[i - 1, "cpi_index"]
            * result.loc[i, "mom_cpi"] / 100
        )

    # 计算以首个月份价格水平为基准的实际消费金额
    base_cpi = result.loc[0, "cpi_index"]

    result["real_expense"] = (
        result["amount"] * base_cpi / result["cpi_index"]
    )

    # 计算个人消费支出环比增长率
    result["expense_growth"] = (
        result["amount"].pct_change() * 100
    )

    # CPI 环比涨幅
    result["cpi_growth"] = (
        result["mom_cpi"] - 100
    )

    st.write("### 名义消费与实际消费对比")

    fig = px.line(
        result,
        x="month",
        y=["amount", "real_expense"],
        markers=True,
        labels={
            "month": "月份",
            "value": "消费金额（元）",
            "variable": "消费类型"
        },
        title="个人名义消费与实际消费变化"
    )

    fig.for_each_trace(
        lambda trace: trace.update(
            name={
                "amount": "名义消费金额",
                "real_expense": "实际消费金额"
            }.get(trace.name, trace.name)
        )
    )

    st.plotly_chart(fig, width="stretch")

    st.write("### CPI 价格指数变化")

    cpi_fig = px.line(
        result,
        x="month",
        y="cpi_index",
        markers=True,
        title="CPI 定基价格指数变化",
        labels={
            "month": "月份",
            "cpi_index": "价格指数（首月=100）"
        }
    )

    st.plotly_chart(cpi_fig, width="stretch")

    st.dataframe(
        result[
            ["month", "amount", "cpi_index", "real_expense"]
        ],
        width="stretch"
    )

    st.write("### 个人消费支出与 CPI 环比涨幅对比")

    growth_data = result.dropna(
        subset=["expense_growth"]
    )

    growth_long = growth_data.melt(
        id_vars=["month"],
        value_vars=["expense_growth", "cpi_growth"],
        var_name="指标",
        value_name="增长率（%）"
    )

    growth_long["指标"] = growth_long["指标"].replace({
        "expense_growth": "个人消费支出环比增长率",
        "cpi_growth": "CPI环比涨幅"
    })

    growth_fig = px.line(
        growth_long,
        x="month",
        y="增长率（%）",
        color="指标",
        markers=True,
        title="个人消费支出与物价涨幅变化对比"
    )

    st.plotly_chart(growth_fig, width="stretch")

def show_economics(data):

    # 经济学指标分析
    st.divider()
    st.subheader("经济学指标分析")

    # 个人消费支出同比增长率
    st.write("### 个人消费支出同比增长率")

    yoy_data = calculate_expense_yoy(data)

    valid_yoy = yoy_data.dropna(
        subset=["yoy_growth"]
    )

    if valid_yoy.empty:
        st.info("暂无足够的去年同期数据，暂时无法计算同比增长率。")
    else:
        yoy_fig = px.bar(
            valid_yoy,
            x="month",
            y="yoy_growth",
            title="个人消费支出同比增长率",
            labels={
                "month": "月份",
                "yoy_growth": "同比增长率（%）"
            }
        )

        st.plotly_chart(yoy_fig, width="stretch")

        st.dataframe(
            yoy_data[
                ["month", "amount", "last_year_amount", "yoy_growth"]
            ],
            width="stretch"
        )

    engel = calculate_engel_coefficient(data)
    apc = calculate_average_propensity_to_consume(data)
    saving_rate = calculate_saving_rate(data)
    mpc = calculate_marginal_propensity_to_consume(data)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("储蓄率", f"{saving_rate * 100:.2f}%")
    col2.metric("恩格尔系数", f"{engel:.2f}%")
    col3.metric("平均消费倾向（APC）", f"{apc:.2f}")

    if mpc is not None:
        col4.metric("边际消费倾向（MPC）", f"{mpc:.3f}")
    else:
        col4.metric("边际消费倾向（MPC）", "暂无法计算")

    st.caption(
        "恩格尔系数为食品支出占总消费支出的比例；"
        "APC 为总消费支出与总收入之比；"
        "MPC 根据最近两个有数据月份的消费和收入变化计算。"
    )

    with st.expander("查看经济学指标说明"):
        st.markdown("""
        - **储蓄率**：收支结余占总收入的比例，反映收入中用于储蓄的部分。计算公式：储蓄率 =（总收入 - 总支出）/ 总收入 × 100%。
        - **恩格尔系数**：食品支出占总消费支出的比例，可用于观察消费结构。
        - **平均消费倾向（APC）**：总消费支出与总收入的比值，反映收入中用于消费的比例。
        - **边际消费倾向（MPC）**：收入变化量中用于增加消费的比例，根据最近两个有数据月份的收入和消费支出变化计算。

        注意：当前指标基于账单记录计算，结果受数据完整性和分类准确性影响。当总收入不大于0时，储蓄率和APC暂返回0。
        """)

    return engel, apc, saving_rate, mpc