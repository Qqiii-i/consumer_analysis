import streamlit as st
from ui.data_import import show_data_import

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

/* 上传成功后的文件信息小框 */
[data-testid="stFileChip"] {
    background-color: #EAF2F8 !important;
    border: 1px solid #D3E0EA !important;
    border-radius: 6px !important;
}

/* 文件名和文件大小 */
[data-testid="stFileChip"] * {
    color: #FFFFFF !important;
}

[data-testid="stFileChipName"],
[data-testid="stFileChipName"] + div {
    color: #000000 !important;
}

[data-testid="stFileUploader"] button svg {
    fill: #FFFFFF !important;
    color: #FFFFFF !important;
}

/* 普通按钮 */
.stButton button {
    background-color: #EAF2F8 !important;
    color: #253247 !important;
    border: 1px solid #D3E0EA !important;
}

</style>
""", unsafe_allow_html=True)

st.title(":material/folder_open: 数据导入与清洗")

st.markdown("""
<style>
.stApp h1,
a[data-testid="stPageLink-NavLink"] p {
    color: #000000;
}
</style>
""", unsafe_allow_html=True)

show_data_import()

st.divider()

st.page_link(
    "pages/home.py",
    label="返回首页",
    icon=":material/home:",
    width="stretch"
)

st.page_link(
    "pages/classification.py",
    label="前往自动消费分类",
    icon=":material/arrow_forward:",
    width="stretch"
)