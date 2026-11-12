import streamlit as st

st.markdown(
    """
    <div style="text-align: center;">
        <h1 style="font-size: 45px; color: black;">
            消费分析中心
        </h1>
        <p style="font-size: 15px; letter-spacing: 2px; color: #416482;">
            Personal Finance Analytics Platform
        </p>
        <p style="font-size: 19px; color: black;">
            欢迎使用个人消费行为分析平台。<br>请选择需要使用的功能。
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# 功能入口
st.markdown(
    "<h2 style='color: black;'>功能导航</h2>",
    unsafe_allow_html=True
)

features = [
    ("folder_open", "数据导入与清洗", "导入账单并整理消费数据"),
    ("sell", "自动消费分类", "识别消费记录所属类别"),
    ("query_stats", "经济学分析指标", "分析恩格尔系数、储蓄率等指标"),
    ("trending_up", "CPI 与个人消费分析", "分析物价变化与个人消费"),
    ("pie_chart", "消费统计与趋势分析", "查看消费结构和变化趋势"),
    ("monitoring", "消费预测", "预测未来消费情况"),
    ("search", "异常消费检测", "识别异常消费记录"),
    ("groups", "消费行为聚类", "分析不同消费行为特征"),
    ("description", "分析报告导出", "生成Excel和PDF分析报告"),
]

# 固定三列，所有卡片统一跟随最高卡片的高度
st.markdown("""
<style>
/* 页面整体宽度 */
.block-container {
    max-width: 1600px;
    padding-left: 4rem;
    padding-right: 4rem;
}

/* 每一排卡片等高 */
[data-testid="stColumn"] {
    display: flex;
    flex-direction: column;
}

[data-testid="stColumn"] > div {
    height: 100%;
}

a[data-testid="stPageLink-NavLink"] {
    height: 150px;
    min-height: 150px;
    width: 100%;
}

/* 卡片整体 */
a[data-testid="stPageLink-NavLink"] {
    display: flex;
    align-items: flex-start;
    width: 100%;
    min-height: 135px;
    padding: 22px;
    box-sizing: border-box;

    background: #D3E6F0;
    border: 1px solid #e8edf3;
    border-radius: 14px;

    text-decoration: none;
    transition: all 0.2s ease;
}

/* 确保卡片内部内容可以正常换行 */
a[data-testid="stPageLink-NavLink"] > div {
    width: 100%;
    min-width: 0;
}

/* 标题 */
a[data-testid="stPageLink-NavLink"] p:first-child {
    margin: 0 0 12px 0;
    line-height: 1.5;
    white-space: normal !important;
    overflow-wrap: anywhere;
    word-break: normal;
}

a[data-testid="stPageLink-NavLink"] p:first-child strong {
    display: inline;
    font-size: 18px;
    color: #253247;
    font-weight: 700;
    white-space: normal !important;
    overflow-wrap: anywhere;
    word-break: normal;
}

/* 说明文字 */
a[data-testid="stPageLink-NavLink"] p:last-child {
    margin: 0;
    font-size: 14px;
    line-height: 1.6;
    color: #718096;

    white-space: normal;
    overflow-wrap: break-word;
    word-break: normal;
}

/* 放大功能卡片图标 */
a[data-testid="stPageLink-NavLink"] [data-testid="stIconMaterial"] {
    font-size: 24px !important;
}

/* 鼠标悬停 */
a[data-testid="stPageLink-NavLink"]:hover {
    border-color: #9aabc0;
    background: #f8fafc;
    transform: translateY(-3px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}
</style>
""", unsafe_allow_html=True)

# 生成所有卡片
# 功能页面对应关系
page_paths = {
    "数据导入与清洗": "pages/data_import.py",
    "自动消费分类": "pages/classification.py",
    "经济学分析指标": "pages/economics.py",
    "CPI 与个人消费分析": "pages/cpi.py",
    "消费统计与趋势分析": "pages/statistics.py",
    "消费预测": "pages/forecast.py",
    "异常消费检测": "pages/anomaly.py",
    "消费行为聚类": "pages/clustering.py",
    "分析报告导出": "pages/reports.py"
}

# 三列展示
cols = st.columns(3, gap="medium")

for i, (icon, title, description) in enumerate(features):
    with cols[i % 3]:
        st.page_link(
            page_paths[title],
            label=f"**{title}**\n\n{description}",
            icon=f":material/{icon}:",
            use_container_width=True
        )