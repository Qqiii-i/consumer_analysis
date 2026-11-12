import streamlit as st
import pandas as pd
from algorithms.trend_analysis import(
    generate_consumption_insights,
    predict_next_month_expense
)
from reports.pdf_report import create_pdf_report
from reports.excel_report import create_excel_report

st.title(":material/description: 分析报告导出")

st.markdown("""
<style>
/* 数据表格浅色主题 */
[data-testid="stDataFrame"] {
    --gdg-bg-cell: #FFFFFF;
    --gdg-bg-cell-medium: #F5F8FA;
    --gdg-bg-header: #EAF2F8;
    --gdg-text-dark: #253247;
    --gdg-text-medium: #253247;
    --gdg-border-color: #D3E0EA;
}

/* 页面标题和普通文字 */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp p,
.stApp label,
.stApp span,
.stApp div {
    color: #000000;
}

/* 下载账单模板按钮 */
.stDownloadButton button {
    background-color: #EAF2F8 !important;
    color: #253247 !important;
    border: 1px solid #D3E0EA !important;
}

/* 普通按钮 */
.stButton button {
    background-color: #EAF2F8 !important;
    color: #253247 !important;
    border: 1px solid #D3E0EA !important;
}
</style>
""", unsafe_allow_html=True)

# 检查是否已经完成必要的分析
required_results = {
    "transaction_data": "数据导入与清洗",
    "classified_data": "自动消费分类",
    "economics_results": "经济学分析指标",
    "statistics_results": "消费统计与趋势分析",
    "abnormal_data": "异常消费检测",
    "cluster_summary": "消费行为聚类"
}

missing_results = [
    name
    for key, name in required_results.items()
    if key not in st.session_state
]

if missing_results:
    st.warning("请先完成以下模块，再生成分析报告：")

    for name in missing_results:
        st.write(f"- {name}")

    st.info("完成相应模块后，再返回本页面导出报告。")

else:
    # 获取账单数据
    data = st.session_state["transaction_data"].copy()

    # 获取最终分类结果
    classified_data = st.session_state["classified_data"]

    # 将最终分类结果匹配到原始账单
    category_mapping = classified_data.set_index(
        "transaction_id"
    )["final_category"]

    data["category"] = (
        data["transaction_id"]
        .map(category_mapping)
        .fillna(data["category"])
    )

    # 计算收入、支出和结余
    income = data.loc[
        data["transaction_type"] == "收入", "amount"
    ].sum()

    expense = data.loc[
        data["transaction_type"] == "支出", "amount"
    ].sum()

    balance = income - expense

    # 获取经济学指标
    economics_results = st.session_state["economics_results"]

    engel = economics_results["engel"]
    apc = economics_results["apc"]
    saving_rate = economics_results["saving_rate"]
    mpc = economics_results["mpc"]

    # 获取统计分析结果
    statistics_results = st.session_state["statistics_results"]

    # 计算下个月消费预测
    if len(monthly_trend := st.session_state["statistics_results"]["monthly_trend"]) >= 3:
        forecast_amount = predict_next_month_expense(monthly_trend)

        forecast_month = (
            pd.Period(monthly_trend["month"].iloc[-1], freq="M") + 1
        ).strftime("%Y-%m")
    else:
        forecast_amount = None
        forecast_month = None

    # 获取 CPI 分析结果（可选）
    cpi_results = st.session_state.get("cpi_results")

    category_stats = statistics_results["category_stats"]
    monthly_trend = statistics_results["monthly_trend"]
    moving_average_data = statistics_results["moving_average_data"]

    pie_fig = statistics_results["pie_fig"]
    line_fig = statistics_results["line_fig"]
    bar_fig = statistics_results["bar_fig"]

    # 获取异常检测和聚类结果
    abnormal_data = st.session_state["abnormal_data"]
    cluster_summary = st.session_state["cluster_summary"]
    category_summary = st.session_state.get("category_summary")
    silhouette = st.session_state.get("silhouette")

    st.divider()

    st.subheader("报告内容：")

    st.markdown("""
    - 清洗后的消费账单
    - 收入、支出与收支结余
    - 储蓄率、恩格尔系数、APC 和 MPC
    - CPI与个人消费分析
    - 消费类别统计与月度消费趋势
    - 消费偏好与行为特征分析
    - 移动平均分析与消费预测
    - K-Means 消费行为聚类分析
    """)

    st.divider()

    st.subheader("导出消费分析报告")

    # Excel 报告导出
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
        label=":material/bar_chart: 下载 Excel 消费分析报告",
        data=excel_buffer,
        file_name="消费行为分析报告.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        width="stretch"
    )

    # PDF 报告导出
    if st.button(":material/library_books: 生成PDF消费分析报告", width="stretch"):

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
                cluster_summary,
                moving_average_data,
                pie_fig,
                line_fig,
                bar_fig,
                cpi_results=cpi_results,
                consumption_insights=generate_consumption_insights(
                    st.session_state["transaction_data"]
                ),
                forecast_month=forecast_month,
                forecast_amount=forecast_amount,
                category_summary=category_summary,
                silhouette=silhouette,
                moving_average_fig=st.session_state[
                    "statistics_results"
                ].get("moving_average_fig")
            )

        st.success("PDF 报告生成成功！")

        st.download_button(
            label="下载 PDF 消费分析报告",
            data=pdf_buffer,
            file_name="消费行为分析报告.pdf",
            mime="application/pdf",
            width="stretch"
        )

st.divider()

st.page_link(
    "pages/clustering.py",
    label="返回消费行为聚类",
    icon=":material/arrow_back:",
    width="stretch"
)

st.page_link(
    "pages/home.py", 
    label="返回首页", 
    icon=":material/home:",
    width="stretch"
)