from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .utils import analyze_csv
from .models import EquipmentDataset, UploadHistory

class UploadCSVView(APIView):
    parser_classes=(MultiPartParser, FormParser)
    permission_classes=[AllowAny] #IsAuthenticated later, if needed

    def post(self, request):
        if 'file' not in request.FILES:
            return Response(
                {"error": "No file provided. Use form-data with key file"},
                status=status.HTTP_400_BAD_REQUEST
            )

        file=request.FILES['file']
        summary,df=analyze_csv(file)

        if EquipmentDataset.objects.count()>=5:
            EquipmentDataset.objects.order_by('uploaded_at').first().delete()

        EquipmentDataset.objects.create(
            filename=file.name,
            summary=summary
        )

        UploadHistory.objects.create(
            filename=file.name,
            summary=summary
        )

        # Keep only last 5 uploads
        qs = UploadHistory.objects.order_by("-uploaded_at")
        if qs.count() > 5:
            for obj in qs[5:]:
                obj.delete()

        return Response({
            "summary":summary,
            "table":df.to_dict(orient="records")
        })

# class HistoryView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         datasets = EquipmentDataset.objects.order_by('-uploaded_at')[:5]

#         return Response([
#             {
#                 "filename": d.filename,
#                 "uploaded_at": d.uploaded_at,
#                 "summary": d.summary
#             }
#             for d in datasets
#         ])

class HistoryView(APIView):
    def get(self, request):
        data = UploadHistory.objects.order_by('-uploaded_at').values(
            'filename', 'uploaded_at', 'summary'
        )
        return Response(list(data))

class PDFReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        latest = EquipmentDataset.objects.latest('uploaded_at')

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="equipment_report.pdf"'

        pdf = canvas.Canvas(response)
        pdf.setFont("Helvetica", 12)

        pdf.drawString(50, 800, "Chemical Equipment Summary Report")

        y = 760
        for key, value in latest.summary.items():
            pdf.drawString(50, y, f"{key}: {value}")
            y -= 20

        pdf.showPage()
        pdf.save()

        return response

