import streamlit as st

st.set_page_config(
    page_title="智能消费行为分析平台",
    page_icon="💰",
    layout="wide"
)

# 定义页面
home_page = st.Page(
    "pages/home.py",
    title="首页",
    icon="🏠",
    default=True
)

data_import_page = st.Page(
    "pages/data_import.py",
    title="数据导入与清洗",
    icon="📂"
)

classification_page = st.Page(
    "pages/classification.py",
    title="自动消费分类",
    icon="🏷️"
)

economics_page = st.Page(
    "pages/economics.py",
    title="经济学分析指标",
    icon="📈"
)

# CPI 与个人消费分析
cpi_page = st.Page(
    "pages/cpi.py",
    title="CPI 与个人消费分析",
    icon="📉"
)

# 消费统计与趋势分析
statistics_page = st.Page(
    "pages/statistics.py",
    title="消费统计与趋势分析",
    icon="📊"
)

# 消费预测
forecast_page = st.Page(
    "pages/forecast.py",
    title="消费预测",
    icon="🔮"
)

# 异常消费检测
anomaly_page = st.Page(
    "pages/anomaly.py",
    title="异常消费检测",
    icon="🔍"
)

# 消费行为聚类
clustering_page = st.Page(
    "pages/clustering.py",
    title="消费行为聚类",
    icon="🧩"
)

# 分析报告导出
reports_page = st.Page(
    "pages/reports.py",
    title="分析报告导出",
    icon="📄"
)

# 创建导航
navigation = st.navigation([
    home_page,
    data_import_page,
    classification_page,
    economics_page,
    cpi_page,
    statistics_page,
    forecast_page,
    anomaly_page,
    clustering_page,
    reports_page
])

navigation.run()