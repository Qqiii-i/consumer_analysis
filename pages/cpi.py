import streamlit as st
from ui.economics import show_cpi_analysis

st.title(":material/trending_up: CPI与个人消费分析")

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

else:
    data = st.session_state["transaction_data"].copy()

    cpi_results = show_cpi_analysis(data)

    if cpi_results is not None:
        st.session_state["cpi_results"] = cpi_results

st.divider()

st.page_link(
    "pages/economics.py",
    label="返回经济学分析指标",
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
    "pages/statistics.py",
    label="前往消费统计与趋势分析",
    icon=":material/arrow_forward:",
    width="stretch"
)