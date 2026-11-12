import streamlit as st
from ui.economics import show_economics

st.title(":material/query_stats: 经济学分析指标")

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

/* 经济学指标说明：白底黑字，保留黑色边框 */
[data-testid="stExpander"],
[data-testid="stExpander"] details {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border: 1px solid #000000 !important;
    border-radius: 8px;
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span,
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p,
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] li,
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] strong {
    color: #000000 !important;
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

    # 执行经济学指标分析，并保存报告所需结果
    engel, apc, saving_rate, mpc = show_economics(data)

    st.session_state["economics_results"] = {
        "engel": engel,
        "apc": apc,
        "saving_rate": saving_rate,
        "mpc": mpc
    }

st.divider()

st.page_link(
    "pages/classification.py",
    label="返回自动消费分类",
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
    "pages/cpi.py",
    label="前往 CPI 与个人消费分析",
    icon=":material/arrow_forward:",
    width="stretch"
)