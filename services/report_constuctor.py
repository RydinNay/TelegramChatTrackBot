from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

SYSTEM_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def generate_pdf(
        filename: str,
        title: str,
        period_text: str,
        report_rows: list[dict],
        unsubscribed_count: int,
        active_users_count: int,
        total_count: int
):
    # Регистрируем шрифт
    pdfmetrics.registerFont(TTFont('DejaVu', SYSTEM_FONT_PATH))

    # Базовые стили
    styles = getSampleStyleSheet()
    styles['Normal'].fontName = 'DejaVu'
    styles['Title'].fontName = 'DejaVu'

    pdf = SimpleDocTemplate(filename, pagesize=A4)
    elements = []

    # Заголовок
    elements.append(Paragraph(f"<b>{title}</b>", styles['Title']))
    elements.append(Spacer(1, 10))

    # Период
    elements.append(Paragraph(period_text, styles['Normal']))
    elements.append(Spacer(1, 20))

    # Таблица
    table_data = [["Источник", "Всего", "Отписались", "Активные"]]

    for row in report_rows:
        table_data.append([
            row["source"],
            str(row["total"]),
            str(row["unsubscribed"]),
            str(row["active"])
        ])

    # Итоговая строка
    table_data.append([
        "ИТОГ",
        str(total_count),
        str(unsubscribed_count),
        str(active_users_count)
    ])

    table = Table(table_data)

    # Стиль таблицы
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "DejaVu"),     # Шрифт для всех строк
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.8, colors.grey),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

        # Последняя строка — выделение жирным
        ("FONTNAME", (0, -1), (-1, -1), "DejaVu"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.whitesmoke),
    ]))

    elements.append(table)
    pdf.build(elements)

    return filename
