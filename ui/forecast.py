import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from algorithms.trend_analysis import (
    calculate_monthly_trend,
    calculate_moving_average,
    predict_next_month_expense
)

def show_forecast(data):
    st.subheader("消费移动平均分析")

    monthly_trend = calculate_monthly_trend(data)

    if len(monthly_trend) >= 2:
        moving_average_data = calculate_moving_average(
            monthly_trend,
            window=2
        )

        st.dataframe(
            moving_average_data,
            width="stretch"
        )

        moving_average_fig = px.line(
            moving_average_data,
            x="month",
            y=["total_expense", "moving_average"],
            markers=True,
            title="消费移动平均分析",
            labels={
                "month": "月份",
                "value": "消费金额（元）",
                "variable": "指标"
            }
        )

        # 设置月份标签水平显示
        moving_average_fig.update_xaxes(tickangle=0)

        st.plotly_chart(
            moving_average_fig,
            width="stretch"
        )

        if len(monthly_trend) >= 3:
            prediction = predict_next_month_expense(monthly_trend)

            next_month = (
                pd.Period(monthly_trend["month"].iloc[-1], freq="M") + 1
            ).strftime("%Y-%m")

            st.subheader("下个月消费预测")
            st.metric(
                "预计消费金额",
                f"¥{prediction:,.2f}"
            )

            forecast_fig = go.Figure()

            forecast_fig.add_trace(go.Scatter(
                x=monthly_trend["month"],
                y=monthly_trend["total_expense"],
                mode="lines+markers",
                name="历史实际消费"
            ))

            forecast_fig.add_trace(go.Scatter(
                x=[monthly_trend["month"].iloc[-1], next_month],
                y=[monthly_trend["total_expense"].iloc[-1], prediction],
                mode="lines+markers",
                name="下个月预测消费",
                line=dict(dash="dash")
            ))

            forecast_fig.update_layout(
                title="历史消费与下个月预测对比",
                xaxis_title="月份",
                yaxis_title="消费金额（元）"
            )

            st.plotly_chart(forecast_fig, width="stretch")

        else:
            st.info("至少需要3个月的消费数据才能预测下个月支出。")

    else:
        st.info("月度数据不足2个月，暂时无法进行移动平均分析。")