
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

# 注册中文字体
pdfmetrics.registerFont(
    TTFont("SimHei", r"C:\Windows\Fonts\simhei.ttf")
)


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
    abnormal_data,
    classified_data,
    cluster_summary,
    moving_average_data,
    pie_fig,
    line_fig,
    bar_fig
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
        ["指标名称", "计算结果"],
        ["总收入", f"{income:.2f} 元"],
        ["总支出", f"{expense:.2f} 元"],
        ["收支结余", f"{balance:.2f} 元"],
        ["储蓄率", f"{saving_rate * 100:.2f}%"],
        ["恩格尔系数", f"{engel:.2f}%"],
        ["平均消费倾向（APC）", f"{apc:.3f}"],
        [
            "边际消费倾向（MPC）",
            "暂无法计算" if mpc is None else f"{mpc:.3f}"
        ]
    ]

    table = Table(indicators, colWidths=[220, 220])

    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "SimHei"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("PADDING", (0, 0), (-1, -1), 7),
    ]))

    story.append(table)

    # 插入消费类别占比图
    if pie_fig is not None:
        story.append(
            Paragraph("二、消费类别占比图", heading_style)
        )

        pie_image = Image(
            BytesIO(pie_fig.to_image(format="png")),
            width=400,
            height=280
        )

        story.append(pie_image)
        story.append(Spacer(1, 12))

    # 插入月度消费趋势图
    if line_fig is not None:
        story.append(
            Paragraph("三、月度消费趋势图", heading_style)
        )

        line_image = Image(
            BytesIO(line_fig.to_image(format="png")),
            width=450,
            height=260
        )

        story.append(line_image)
        story.append(Spacer(1, 12))

    # 插入消费类别金额柱状图
    if bar_fig is not None:
        story.append(
            Paragraph("四、消费类别金额统计图", heading_style)
        )

        bar_image = Image(
            BytesIO(bar_fig.to_image(format="png")),
            width=450,
            height=260
        )

        story.append(bar_image)
        story.append(Spacer(1, 12))

    # 添加分析数据表
    report_tables = [
        ("二、消费类别统计", category_stats),
        ("三、月度消费趋势", monthly_trend),
        ("四、异常消费记录", abnormal_data),
        ("五、消费分类结果", classified_data),
        ("六、K-Means 聚类统计", cluster_summary),
        ("七、移动平均分析", moving_average_data)
    ]

    for title, df in report_tables:
        story.append(
            Paragraph(title, heading_style)
        )

        if df.empty:
            story.append(
                Paragraph("暂无可展示的数据。", normal_style)
            )
            continue

        display_df = df.head(30)

        table_data = [
            [str(column) for column in display_df.columns]
        ]

        for _, row in display_df.iterrows():
            table_data.append([
                str(value) for value in row
            ])

        report_table = Table(
            table_data,
            repeatRows=1
        )

        report_table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "SimHei"),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 7),
            ("PADDING", (0, 0), (-1, -1), 4),
        ]))

        story.append(report_table)
        story.append(Spacer(1, 8))

    doc.build(story)

    pdf_buffer.seek(0)

    return pdf_buffer
