import os
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)

font_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "assets",
    "fonts",
    "simhei.ttf"
)

pdfmetrics.registerFont(TTFont("SimHei", font_path))

def create_pdf_report(
    income,
    expense,
    balance,
    saving_rate,
    engel,
    apc,
    mpc,
    category_stats,
    monthly_trend,
    cluster_summary,
    moving_average_data,
    pie_fig,
    line_fig,
    bar_fig,
    cpi_results=None,
    consumption_insights=None,
    forecast_month=None,
    forecast_amount=None,
    category_summary=None,
    silhouette=None,
    moving_average_fig=None
):
    pdf_buffer = BytesIO()

    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ChineseTitle",
        parent=styles["Title"],
        fontName="SimHei",
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=20
    )

    heading_style = ParagraphStyle(
        "ChineseHeading",
        parent=styles["Heading2"],
        fontName="SimHei",
        fontSize=12,
        spaceBefore=12,
        spaceAfter=8
    )

    normal_style = ParagraphStyle(
        "ChineseNormal",
        parent=styles["Normal"],
        fontName="SimHei",
        fontSize=9,
        leading=14
    )

    story = []

    story.append(
        Paragraph("智能消费行为分析报告", title_style)
    )

    story.append(
        Paragraph("一、经济学指标", heading_style)
    )

    indicators = [
        ["Indicator", "Value"],
        ["Total Income", f"{income:.2f} CNY"],
        ["Total Expenses", f"{expense:.2f} CNY"],
        ["Balance", f"{balance:.2f} CNY"],
        ["Saving Rate", f"{saving_rate * 100:.2f}%"],
        ["Engel Coefficient", f"{engel:.2f}%"],
        ["Average Propensity to Consume(APC)", f"{apc:.3f}"],
        [
            "Marginal Propensity to Consume(MPC)",
            "暂无法计算" if mpc is None else f"{mpc:.3f}"
        ]
    ]

    table = Table(indicators, colWidths=[220, 220])

    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "SimHei"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("PADDING", (0, 0), (-1, -1), 7),
    ]))

    story.append(table)
    
    # 插入 CPI 分析图表
    if cpi_results is not None:
        story.append(
            Paragraph("二、CPI 与个人消费分析", heading_style)
        )

        # 1. CPI 与个人消费分析数据表
        if cpi_results.get("result") is not None:
            story.append(
                Paragraph("1.CPI 与个人消费分析数据表", normal_style)
            )

            cpi_report_data = cpi_results["result"][
                [
                    "month",
                    "amount",
                    "cpi_index",
                    "real_expense",
                    "expense_growth",
                    "cpi_growth"
                ]
            ].copy()

            cpi_report_data = cpi_report_data.round(2).fillna("—")

            cpi_table_data = [
                [str(column) for column in cpi_report_data.columns]
            ]

            for _, row in cpi_report_data.iterrows():
                cpi_table_data.append([
                    str(value) for value in row
                ])

            cpi_table = Table(
                cpi_table_data,
                repeatRows=1
            )

            cpi_table.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, -1), "SimHei"),
                ("BACKGROUND", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("FONTSIZE", (0, 0), (-1, -1), 7),
                ("PADDING", (0, 0), (-1, -1), 4),
            ]))

            story.append(cpi_table)
            story.append(Spacer(1, 12))

        # 2. 名义消费与实际消费对比图
        if cpi_results.get("fig") is not None:
            story.append(
                Paragraph("2.名义消费与实际消费对比", normal_style)
            )

            cpi_image = Image(
                BytesIO(cpi_results["fig"].to_image(format="png")),
                width=450,
                height=260
            )

            story.append(cpi_image)
            story.append(Spacer(1, 12))

        # 3. CPI 价格指数变化图
        if cpi_results.get("cpi_fig") is not None:
            story.append(
                Paragraph("3.CPI价格指数变化", normal_style)
            )

            cpi_index_image = Image(
                BytesIO(cpi_results["cpi_fig"].to_image(format="png")),
                width=450,
                height=260
            )

            story.append(cpi_index_image)
            story.append(Spacer(1, 12))

        # 4. 个人消费支出与 CPI 环比涨幅对比图
        if cpi_results.get("growth_fig") is not None:
            story.append(
                Paragraph("4.个人消费支出与CPI环比涨幅对比", normal_style)
            )

            growth_image = Image(
                BytesIO(cpi_results["growth_fig"].to_image(format="png")),
                width=450,
                height=260
            )

            story.append(growth_image)
            story.append(Spacer(1, 12))

    # 插入消费类别金额柱状图
    if bar_fig is not None:
        story.append(
            Paragraph("三、消费类别金额统计图", heading_style)
        )

        bar_image = Image(
            BytesIO(bar_fig.to_image(format="png")),
            width=450,
            height=260
        )

        story.append(bar_image)
        story.append(Spacer(1, 12))

    # 插入消费类别占比图
    if pie_fig is not None:
        story.append(
            Paragraph("四、消费类别占比图", heading_style)
        )

        pie_image = Image(
            BytesIO(pie_fig.to_image(format="png")),
            width=400,
            height=280
        )

        story.append(pie_image)
        story.append(Spacer(1, 12))
    
    # 插入月度消费趋势
    if line_fig is not None:
        story.append(
            Paragraph("五、月度消费趋势", heading_style)
        )

        # 1. 月度消费趋势表
        story.append(
            Paragraph("1.月度消费趋势表", normal_style)
        )

        trend_table_data = [
            [str(column) for column in monthly_trend.columns]
        ]

        for _, row in monthly_trend.iterrows():
            trend_table_data.append([
                str(value) for value in row
            ])

        trend_table = Table(
            trend_table_data,
            repeatRows=1
        )

        trend_table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "SimHei"),
            ("BACKGROUND", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("PADDING", (0, 0), (-1, -1), 5),
        ]))

        story.append(trend_table)
        story.append(Spacer(1, 12))

        # 2. 月度消费趋势图
        story.append(
            Paragraph("2.月度消费趋势图", normal_style)
        )

        line_image = Image(
            BytesIO(line_fig.to_image(format="png")),
            width=450,
            height=260
        )

        story.append(line_image)
        story.append(Spacer(1, 12))

    # 插入消费偏好与行为特征分析
    if consumption_insights:
        story.append(
            Paragraph("六、消费偏好与行为特征分析", heading_style)
        )

        for insight in consumption_insights:
            story.append(
                Paragraph(
                    f"- {insight}",
                    normal_style
                )
            )
            story.append(Spacer(1, 5))

        story.append(Spacer(1, 12))

    # 插入消费预测分析
    story.append(
        Paragraph("七、消费预测分析", heading_style)
    )

    if forecast_amount is not None:
        forecast_text = (
            f"- 预测月份：{forecast_month}<br/>"
            f"- 预计消费金额：{forecast_amount:,.2f}元"
        )
    else:
        forecast_text = "月度消费数据不足3个月，暂时无法进行下个月消费预测。"

    # 移动平均分析折线图
    if moving_average_fig is not None:
        story.append(
            Paragraph("- 移动平均分析", normal_style)
        )

        moving_average_image = Image(
            BytesIO(
                moving_average_fig.to_image(format="png")
            ),
            width=450,
            height=260
        )

        story.append(moving_average_image)
        story.append(Spacer(1, 12))

    story.append(
        Paragraph(forecast_text, normal_style)
    )

    story.append(Spacer(1, 12))

    # 插入消费行为聚类分析
    story.append(
        Paragraph("八、K-Means 消费行为聚类分析", heading_style)
    )

    if (
        cluster_summary is not None
        and not cluster_summary.empty
        and category_summary is not None
        and not category_summary.empty
    ):
        # 展示聚类轮廓系数
        if silhouette is not None:
            story.append(
                Paragraph(
                    f"- 聚类轮廓系数：{silhouette:.3f}",
                    normal_style
                )
            )
        else:
            story.append(
                Paragraph("当前数据无法计算聚类轮廓系数。", normal_style)
            )

        story.append(Spacer(1, 8))

        # 计算整体平均单笔消费金额
        overall_average = (
            cluster_summary["total_amount"].sum()
            / cluster_summary["transaction_count"].sum()
        )

        story.append(
            Paragraph("1.消费群体特征分析", normal_style)
        )

        # 分析每个聚类组的消费特征
        for _, cluster in cluster_summary.iterrows():
            cluster_id = cluster["cluster"]

            group_categories = category_summary[
                category_summary["cluster"] == cluster_id
            ]

            dominant_category = group_categories.loc[
                group_categories["category_ratio"].idxmax()
            ]

            average_amount = cluster["average_amount"]

            if average_amount > overall_average:
                spending_level = "平均单笔消费金额较高"
            elif average_amount < overall_average:
                spending_level = "平均单笔消费金额较低"
            else:
                spending_level = "平均单笔消费金额接近整体水平"

            insight = (
                f"Cluster {cluster_id}：{spending_level}，"
                f"主要消费类别为{dominant_category['category']}，"
                f"占该组消费金额的"
                f"{dominant_category['category_ratio']:.1f}%。"
            )

            story.append(
                Paragraph(insight, normal_style)
            )
            story.append(Spacer(1, 5))

        story.append(Spacer(1, 12))

        # 各聚类组消费类别分布表
        story.append(
            Paragraph("2.各聚类组消费类别分布", normal_style)
        )

        category_table_data = [
            ["Cluster", "Category", "Expense Amount(CNY)", "Category Proportion(%)"]
        ]

        for _, row in category_summary.iterrows():
            category_table_data.append([
                str(row["cluster"]),
                str(row["category"]),
                f"{row['amount']:.2f}",
                f"{row['category_ratio']:.2f}"
            ])

        category_table = Table(
            category_table_data,
            repeatRows=1
        )

        category_table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "SimHei"),
            ("BACKGROUND", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("PADDING", (0, 0), (-1, -1), 5),
        ]))

        story.append(category_table)
        story.append(Spacer(1, 12))

        # 3. K-Means 聚类统计表
        story.append(
            Paragraph("3.K-Means 聚类统计表", normal_style)
        )

        cluster_table_data = [
            ["Cluster", "Transaction Count", "Average Amount(CNY)", "Total Amount(CNY)"]
        ]

        for _, row in cluster_summary.iterrows():
            cluster_table_data.append([
                str(row["cluster"]),
                str(row["transaction_count"]),
                f"{row['average_amount']:.2f}",
                f"{row['total_amount']:.2f}"
            ])

        cluster_table = Table(
            cluster_table_data,
            repeatRows=1
        )

        cluster_table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "SimHei"),
            ("BACKGROUND", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("PADDING", (0, 0), (-1, -1), 5),
        ]))

        story.append(cluster_table)
        story.append(Spacer(1, 12))

    else:
        story.append(
            Paragraph(
                "消费记录不足，暂时无法进行消费行为聚类分析。",
                normal_style
            )
        )

        story.append(Spacer(1, 12))

    doc.build(story)

    pdf_buffer.seek(0)

    return pdf_buffer