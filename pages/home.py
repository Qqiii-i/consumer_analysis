
import streamlit as st

# 首页标题
st.markdown("# 💰 消费分析中心")
st.caption("PERSONAL FINANCE · ANALYTICS PLATFORM")

st.write("欢迎使用个人消费行为分析平台。请选择需要使用的功能。")

st.divider()

# 功能入口
st.markdown("## 功能导航")

features = [
    ("📂", "数据导入与清洗", "导入账单并整理消费数据"),
    ("🏷️", "自动消费分类", "识别消费记录所属类别"),
    ("📈", "经济学分析指标", "分析恩格尔系数、储蓄率等指标"),
    ("📉", "CPI 与个人消费分析", "分析物价变化与个人消费"),
    ("📊", "消费统计与趋势分析", "查看消费结构和变化趋势"),
    ("🔮", "消费预测", "预测未来消费情况"),
    ("🔍", "异常消费检测", "识别异常消费记录"),
    ("🧩", "消费行为聚类", "分析不同消费行为特征"),
    ("📄", "分析报告导出", "生成 Excel 和 PDF 分析报告"),
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

    background: #ffffff;
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
    font-size: 20px;
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
            label=f"**{icon} {title}**\n\n{description}",
            use_container_width=True
        )