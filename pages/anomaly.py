import streamlit as st
from ui.anomaly import show_anomaly_detection

st.title(":material/search: 异常消费检测")


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

    # 使用最终分类结果
    if "classified_data" in st.session_state:
        classified_data = st.session_state["classified_data"]

        category_mapping = classified_data.set_index(
            "transaction_id"
        )["final_category"]

        data["category"] = (
            data["transaction_id"]
            .map(category_mapping)
            .fillna(data["category"])
        )

    # 执行异常消费检测
    abnormal_data = show_anomaly_detection(data)

    st.session_state["abnormal_data"] = abnormal_data.copy()

st.divider()

st.page_link(
    "pages/forecast.py",
    label="返回消费预测",
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
    "pages/clustering.py",
    label="前往消费行为聚类",
    icon=":material/arrow_forward:",
    width="stretch"
)