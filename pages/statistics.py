import streamlit as st
from ui.statistics import show_statistics

st.title("📊 消费统计与趋势分析")

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

    # 执行统计分析
    (
        category_stats,
        monthly_trend,
        moving_average_data,
        pie_fig,
        line_fig,
        bar_fig
    ) = show_statistics(data)

    # 保存报告所需的统计结果
    st.session_state["statistics_results"] = {
        "category_stats": category_stats,
        "monthly_trend": monthly_trend,
        "moving_average_data": moving_average_data,
        "pie_fig": pie_fig,
        "line_fig": line_fig,
        "bar_fig": bar_fig
    }

st.divider()

st.page_link(
    "pages/cpi.py",
    label="返回CPI与个人消费分析",
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
    "pages/forecast.py",
    label="前往消费预测",
    icon="➡️",
    width="stretch"
)