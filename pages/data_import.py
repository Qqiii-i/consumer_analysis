import streamlit as st
from ui.data_import import show_data_import

st.title("📂 数据导入与清洗")

show_data_import()

st.divider()

st.page_link("pages/home.py", label="返回首页", icon="🏠")