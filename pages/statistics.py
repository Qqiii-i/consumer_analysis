import streamlit as st
from ui.statistics import show_statistics

st.title(":material/pie_chart: 消费统计与趋势分析")

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

/* 上传文件区域 */
[data-testid="stFileUploader"] section {
    background-color: #F5F8FA !important;
    border: 1px dashed #B8C9D6 !important;
    border-radius: 8px;
}


/* Upload 上传按钮 */
[data-testid="stFileUploader"] button {
    background-color: #EAF2F8 !important;
    color: #253247 !important;
    border: 1px solid #B8C9D6 !important;
}

</style>
""", unsafe_allow_html=True)

if "transaction_data" not in st.session_state:
    st.warning("请先进入「数据导入与清洗」上传账单。")
    st.page_link("pages/data_import.py", label="前往数据导入", icon=":material/folder_open:")

elif "classified_data" not in st.session_state:
    st.warning("请先进入「自动消费分类」完成消费分类。")
    st.page_link("pages/classification.py", label="前往自动消费分类", icon=":material/sell:")

else:
    data = st.session_state["transaction_data"].copy()
    classified_data = st.session_state["classified_data"]

    category_mapping = classified_data.set_index(
        "transaction_id"
    )["final_category"]

    data["category"] = (
        data["transaction_id"]
        .map(category_mapping)
        .fillna(data["category"])
    )

    # 排除未分类和缺失分类的交易记录
    data = data[
        data["category"].notna()
        & (data["category"] != "未分类")
    ].copy()

    # 执行统计分析
    (
        category_stats,
        monthly_trend,
        moving_average_data,
        pie_fig,
        line_fig,
        bar_fig,
        moving_average_fig
    ) = show_statistics(data)

    # 保存报告所需的统计结果
    st.session_state["statistics_results"] = {
        "category_stats": category_stats,
        "monthly_trend": monthly_trend,
        "moving_average_data": moving_average_data,
        "pie_fig": pie_fig,
        "line_fig": line_fig,
        "bar_fig": bar_fig,
        "moving_average_fig":moving_average_fig
    }

st.divider()

st.page_link(
    "pages/cpi.py",
    label="返回CPI与个人消费分析",
    icon=":material/arrow_back:",
    width="stretch"
)

st.page_link(
    "pages/home.py",
    label="返回首页",
    icon=":material/home:",
    width="stretch"
)

st.page_link(
    "pages/forecast.py",
    label="前往消费预测",
    icon=":material/arrow_forward:",
    width="stretch"
)