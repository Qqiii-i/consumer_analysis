from io import BytesIO
import pandas as pd

def create_excel_report(
    data,
    income,
    expense,
    balance,
    saving_rate,
    engel,
    apc,
    mpc,
    category_stats,
    monthly_trend,
    abnormal_data,
    classified_data,
    cluster_summary,
    moving_average_data
):
    excel_buffer = BytesIO()

    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:

        # 清洗后的账单
        data.to_excel(
            writer,
            sheet_name="清洗后账单",
            index=False
        )

        # 经济学指标
        indicators_data = pd.DataFrame({
            "指标名称": [
                "总收入",
                "总支出",
                "收支结余",
                "储蓄率",
                "恩格尔系数",
                "平均消费倾向（APC）",
                "边际消费倾向（MPC）"
            ],
            "计算结果": [
                income,
                expense,
                balance,
                saving_rate,
                engel,
                apc,
                mpc
            ]
        })

        indicators_data.to_excel(
            writer,
            sheet_name="经济学指标",
            index=False
        )

        # 消费类别统计
        category_stats.to_excel(
            writer,
            sheet_name="消费类别统计",
            index=False
        )

        # 月度消费趋势
        monthly_trend.to_excel(
            writer,
            sheet_name="月度消费趋势",
            index=False
        )

        # 异常消费记录
        if abnormal_data.empty:
            pd.DataFrame({
                "说明": ["本次未检测到统计异常记录。"]
            }).to_excel(
                writer,
                sheet_name="异常消费记录",
                index=False
            )
        else:
            abnormal_data.to_excel(
                writer,
                sheet_name="异常消费记录",
                index=False
            )

        # 自动分类结果
        classified_data.to_excel(
            writer,
            sheet_name="消费分类结果",
            index=False
        )

        # 聚类分析结果
        if cluster_summary.empty:
            pd.DataFrame({
                "说明": ["消费记录不足3条，暂时无法进行K-Means聚类。"]
            }).to_excel(
                writer,
                sheet_name="聚类统计",
                index=False
            )
        else:
            cluster_summary.to_excel(
                writer,
                sheet_name="聚类统计",
                index=False
            )

        # 移动平均
        if moving_average_data.empty:
            pd.DataFrame({
                "说明": ["月度数据不足2个月，暂时无法进行移动平均分析。"]
            }).to_excel(
                writer,
                sheet_name="移动平均分析",
                index=False
            )
        else:
            moving_average_data.to_excel(
                writer,
                sheet_name="移动平均分析",
                index=False
            )

    excel_buffer.seek(0)

    return excel_buffer
