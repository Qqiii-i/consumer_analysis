import streamlit as st
import pandas as pd
import plotly.express as px
from algorithms.trend_analysis import (
    calculate_monthly_trend,
    calculate_moving_average,
    calculate_expense_by_period,
    calculate_expense_frequency,
    calculate_expense_distribution,
)


def show_statistics(data):
    # 初始化 PDF 所需的图表变量
    pie_fig = None
    line_fig = None
    bar_fig = None

    # 消费类别统计
    st.divider()
    st.subheader("消费类别统计")

    expense_data = data[
        data["transaction_type"] == "支出"
    ]

    category_stats = (
        expense_data.groupby("category")["amount"]
        .sum()
        .reset_index()
        .sort_values("amount", ascending=False)
    )

    if not category_stats.empty:
        bar_fig = px.bar(
            category_stats,
            x="category",
            y="amount",
            title="各类消费金额统计",
            labels={
                "category": "消费类别",
                "amount": "消费金额（元）"
            },
            text="amount",
            color="category",
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        st.plotly_chart(bar_fig, width="stretch")
    else:
        st.info("暂无消费支出数据，无法生成消费类别统计图。")

    # 消费类别占比饼图
    st.subheader("消费类别占比")

    if not category_stats.empty:
        pie_fig = px.pie(
            category_stats,
            names="category",
            values="amount",
            title="各类消费支出占比",
            hole=0.4,
            color="category",
            color_discrete_sequence=px.colors.qualitative.Set2
        )

        pie_fig.update_traces(
            textinfo="label+percent",
            marker=dict(line=dict(color="white", width=2))
        )

        st.plotly_chart(pie_fig, width="stretch")
    else:
        st.info("暂无消费类别数据，无法生成占比图。")

    # 消费结构随时间变化
    st.divider()
    st.subheader("消费结构随时间变化")
    
    monthly_category = expense_data.copy()

    monthly_category["month"] = (
        pd.to_datetime(monthly_category["transaction_date"])
        .dt.to_period("M")
        .astype(str)
    )

    monthly_category = (
        monthly_category.groupby(
            ["month", "category"]
        )["amount"]
        .sum()
        .reset_index()
    )

    if not monthly_category.empty:
        amount_fig = px.line(
            monthly_category,
            x="month",
            y="amount",
            color="category",
            markers=True,
            title="各类别月度消费金额变化",
            labels={
                "month": "月份",
                "amount": "消费金额（元）",
                "category": "消费类别"
            }
        )

        st.plotly_chart(amount_fig, width="stretch")
    else:
        st.info("暂无数据，无法分析消费结构变化。")

     # 消费趋势统计
    st.divider()
    st.subheader("消费趋势统计")

    period_options = {
        "日统计": "D",
        "周统计": "W",
        "月统计": "M",
        "年统计": "Y"
    }

    selected_period = st.selectbox(
        "请选择统计周期",
        options=list(period_options.keys()),
        index=2
    )

    period_code = period_options[selected_period]

    period_data = calculate_expense_by_period(
        data,
        period=period_code
    )

    frequency_data = calculate_expense_frequency(
        data,
        period=period_code
    )

    distribution_data = calculate_expense_distribution(
        data,
        period=period_code
    )

    if len(period_data) >= 2:
        line_fig = px.line(
            period_data,
            x="period",
            y="total_expense",
            markers=True,
            title=f"{selected_period}消费趋势",
            labels={
                "period": "统计时间",
                "total_expense": "消费金额（元）"
            }
        )

        line_fig.update_traces(
            line=dict(color="#2878D0", width=3),
            marker=dict(color="#2878D0", size=8)
        )

        st.plotly_chart(line_fig, width="stretch")

    else:
        st.info(f"目前只有一个{selected_period}的数据，暂时无法比较变化。")
        st.dataframe(period_data, width="stretch")

    # 消费频率
    st.subheader(f"{selected_period}消费频率")

    st.dataframe(
        frequency_data.rename(
            columns={
                "period": "统计时间",
                "transaction_count": "消费次数"
            }
        ),
        width="stretch"
    )

    # 消费金额分布
    if period_code in ["M", "Y"]:
        st.subheader("消费金额分布")

        distribution_period_options = sorted(
            distribution_data["period"].dropna().unique().tolist()
        )

        if distribution_period_options:
            selected_distribution_period = st.selectbox(
                "请选择要查看的时间",
                distribution_period_options,
                format_func=lambda x: (
                    f"{x}年" if period_code == "Y"
                    else f"{x[:4]}年{x[5:]}月"
                ),
                key=f"distribution_period_{period_code}"
            )

            selected_distribution_data = distribution_data[
                distribution_data["period"] == selected_distribution_period
            ]

            distribution_summary = (
                selected_distribution_data.groupby(
                    "amount_range",
                    observed=False
                )["transaction_count"]
                .sum()
                .reset_index()
            )

            total_count = int(
                distribution_summary["transaction_count"].sum()
            )

            st.metric("消费总笔数", total_count)

            distribution_fig = px.bar(
                distribution_summary,
                x="amount_range",
                y="transaction_count",
                title="不同金额区间的消费笔数",
                labels={
                    "amount_range": "金额区间",
                    "transaction_count": "消费笔数"
                },
                text="transaction_count"
            )

            st.plotly_chart(distribution_fig, width="stretch")
        else:
            st.info("当前没有可用于金额分布统计的支出数据。")

    # 保留移动平均数据，供报告导出使用
    monthly_trend = calculate_monthly_trend(data)

    if len(monthly_trend) >= 2:
        moving_average_data = calculate_moving_average(
            monthly_trend,
            window=2
        )
    else:
        moving_average_data = pd.DataFrame(
            columns=["month", "total_expense", "moving_average"]
        )

    return (
        category_stats,
        monthly_trend,
        moving_average_data,
        pie_fig,
        line_fig,
        bar_fig
    )
