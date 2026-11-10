import streamlit as st
from ui.classification import show_classification

st.title("🏷️ 自动消费分类")

# 获取数据导入页面保存的账单
if "transaction_data" not in st.session_state:
    st.warning("请先进入「数据导入与清洗」上传账单。")
    st.page_link("pages/data_import.py", label="前往数据导入", icon="📂")

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
    "pages/economics.py",
    label="前往经济学分析指标",
    icon="➡️",
    width="stretch"
)