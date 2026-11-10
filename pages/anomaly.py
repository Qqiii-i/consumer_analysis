import streamlit as st
from ui.anomaly import show_anomaly_detection

st.title("🔍 异常消费检测")

if "transaction_data" not in st.session_state:
    st.warning("请先进入「数据导入与清洗」上传账单。")
    st.page_link("pages/data_import.py", label="前往数据导入", icon="📂")

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
    "pages/clustering.py",
    label="前往消费行为聚类",
    icon="➡️",
    width="stretch"
)