import streamlit as st
from ui.economics import show_economics

st.title("📈 经济学分析指标")

if "transaction_data" not in st.session_state:
    st.warning("请先进入「数据导入与清洗」上传账单。")
    st.page_link("pages/data_import.py", label="前往数据导入", icon="📂")

elif "classified_data" not in st.session_state:
    st.warning("请先进入「自动消费分类」完成消费分类。")
    st.page_link("pages/classification.py", label="前往自动消费分类", icon="🏷️")

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
    "pages/cpi.py",
    label="前往 CPI 与个人消费分析",
    icon="➡️",
    width="stretch"
)