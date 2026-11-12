import streamlit as st
from ui.classification import show_classification

st.title(":material/sell: 自动消费分类")

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

# 获取数据导入页面保存的账单
if "transaction_data" not in st.session_state:
    st.warning("请先进入「数据导入与清洗」上传账单。")
    st.page_link("pages/data_import.py", label="前往数据导入", icon=":material/folder_open:")

else:
    data = st.session_state["transaction_data"]

    # 执行自动消费分类
    classified_data = show_classification(data)

    # 保存分类结果，供其他分析模块使用
    st.session_state["classified_data"] = classified_data.copy()

st.divider()

st.page_link(
    "pages/data_import.py",
    label="返回数据导入与清洗",
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
    "pages/economics.py",
    label="前往经济学分析指标",
    icon=":material/arrow_forward:",
    width="stretch"
)