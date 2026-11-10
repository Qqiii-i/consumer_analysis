import streamlit as st
import pandas as pd
from reports.pdf_report import create_pdf_report
from reports.excel_report import create_excel_report
from ui.statistics import show_statistics
from ui.forecast import show_forecast
from ui.data_import import show_data_import
from ui.economics import show_economics
from ui.economics import show_cpi_analysis
from ui.anomaly import show_anomaly_detection
from ui.classification import show_classification
from ui.clustering import show_clustering

# 网页基本配置
st.set_page_config(
    page_title="智能消费行为分析平台",
    page_icon="💰",
    layout="wide"
)

# 自定义页面样式
st.markdown("""
<style>
    .stApp {
        background-color: #416482;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    h1, h2, h3 {
        color: #253247;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #edf0f5;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(30, 50, 80, 0.04);
    }
</style>
""", unsafe_allow_html=True)

# 顶部欢迎区域
header_left = st.container()

with header_left:
    st.markdown("## 💰 消费分析中心")
    st.caption("PERSONAL FINANCE · ANALYTICS DASHBOARD")
    st.write("欢迎回来，查看你的消费情况和财务变化。")

st.divider()

# 数据导入与清洗
with st.expander("📂 数据导入与清洗", expanded=True):
    data = show_data_import()

# 收入、支出和结余统计
income = data.loc[
    data["transaction_type"] == "收入", "amount"
].sum()

expense = data.loc[
    data["transaction_type"] == "支出", "amount"
].sum()

balance = income - expense

st.divider()
st.markdown("## 财务概览")
st.caption("FINANCIAL OVERVIEW · 收入、支出与结余")

col1, col2, col3 = st.columns(3)

col1.metric("总收入", f"¥{income:,.2f}")
col2.metric("总支出", f"¥{expense:,.2f}")
col3.metric("收支结余", f"¥{balance:,.2f}")

# 自动消费分类
with st.expander("🏷️ 自动消费分类", expanded=True):
    classified_data = show_classification(data)

# 使用人工确认后的最终类别
analysis_data = data.copy()
analysis_data["category"] = classified_data["final_category"].values

# 经济学指标分析
with st.expander("📈 经济学指标分析", expanded=True):
    engel, apc, saving_rate, mpc = show_economics(analysis_data)

# CPI 物价指数与个人消费分析
with st.expander("📉 CPI物价指数与个人消费分析", expanded=True):
    show_cpi_analysis(analysis_data)

# 消费统计与趋势分析
with st.expander("📊 消费统计与趋势分析", expanded=True):
    (
        category_stats,
        monthly_trend,
        moving_average_data,
        pie_fig,
        line_fig,
        bar_fig
    ) = show_statistics(analysis_data)

# 消费预测
with st.expander("🔮 消费预测", expanded=False):
    show_forecast(analysis_data)

# 异常消费检测
with st.expander("🔍 异常消费检测", expanded=True):
    abnormal_data = show_anomaly_detection(analysis_data)

# K-Means消费行为聚类
with st.expander("🧩 K-Means消费行为聚类", expanded=True):
    cluster_summary = show_clustering(analysis_data)

# Excel 分析报告导出
st.divider()
st.subheader("导出消费分析报告")

excel_buffer = create_excel_report(
    data,
    income,
    expense,
    balance,
    saving_rate,
    engel,
    apc,
    mpc,
    category_stats,
    monthly_trend,
    abnormal_data,
    classified_data,
    cluster_summary,
    moving_average_data
)

st.download_button(
    label="下载 Excel 消费分析报告",
    data=excel_buffer,
    file_name="消费行为分析报告.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    width="stretch"
)

# PDF 分析报告导出
if st.button("生成 PDF 消费分析报告", width="stretch"):

    with st.spinner("正在生成 PDF 报告，请稍候..."):

        pdf_buffer = create_pdf_report(
            income,
            expense,
            balance,
            saving_rate,
            engel,
            apc,
            mpc,
            category_stats,
            monthly_trend,
            abnormal_data,
            classified_data,
            cluster_summary,
            moving_average_data,
            pie_fig,
            line_fig,
            bar_fig
        )

    st.success("PDF 报告生成成功！")

    st.download_button(
        label="下载 PDF 消费分析报告",
        data=pdf_buffer,
        file_name="消费行为分析报告.pdf",
        mime="application/pdf",
        width="stretch"
    )