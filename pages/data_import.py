import streamlit as st
from ui.data_import import show_data_import

st.title("📂 数据导入与清洗")

show_data_import()

st.divider()

st.page_link(
    "pages/home.py",
    label="返回首页",
    icon="🏠",
    width="stretch"
)

st.page_link(
    "pages/classification.py",
    label="前往自动消费分类",
    icon="➡️",
    width="stretch"
)