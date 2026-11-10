import streamlit as st
from ui.economics import show_cpi_analysis

st.title("📉 CPI 与个人消费分析")

if "transaction_data" not in st.session_state:
    st.warning("请先进入「数据导入与清洗」上传账单。")
    st.page_link("pages/data_import.py", label="前往数据导入", icon="📂")

else:
    data = st.session_state["transaction_data"].copy()

    show_cpi_analysis(data)

st.divider()

st.page_link(
    "pages/economics.py",
    label="返回经济学分析指标",
    icon="⬅️",
    width="stretch"
)

st.page_link(
    "pages/home.py",
    label="返回首页",
    icon="🏠",
    width="stretch"
)

st.page_link(
    "pages/statistics.py",
    label="前往消费统计与趋势分析",
    icon="➡️",
    width="stretch"
)