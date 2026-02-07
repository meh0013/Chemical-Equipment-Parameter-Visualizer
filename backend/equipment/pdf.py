# equipment/pdf.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def generate_pdf(summary):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    c = canvas.Canvas(response, pagesize=A4)
    text = c.beginText(40, 800)

    text.textLine("Equipment Data Report")
    text.textLine("")
    text.textLine(f"Total Equipment: {summary['total_equipment']}")
    text.textLine(f"Avg Flowrate: {summary['average_flowrate']}")
    text.textLine(f"Avg Pressure: {summary['average_pressure']}")
    text.textLine(f"Avg Temperature: {summary['average_temperature']}")

    if 'type_distribution' in summary:
        text.textLine("")
        text.textLine("Equipment Type Distribution:")
        for t, count in summary['type_distribution'].items():
            text.textLine(f"{t}: {count}")

    c.drawText(text)
    c.showPage()
    c.save()

    return response
