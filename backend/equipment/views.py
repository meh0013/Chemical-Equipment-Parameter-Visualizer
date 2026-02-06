from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .utils import analyze_csv
from .models import EquipmentDataset

class UploadCSVView(APIView):
    parser_classes=(MultiPartParser, FormParser)
    permission_classes=[IsAuthenticated]

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

        return Response({
            "summary":summary,
            "table":df.to_dict(orient="records")
        })

class HistoryView(APIView):
    def get(self,request):
        data=Equipment.objects.order_by('-uploadedDate')[:5]
        return Response([{
                "file": d.filename,
                "uploadedDate": d.uploaded_at,
                "summary": d.summary
            } for d in data])

class PDFReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        latest = EquipmentDataset.objects.latest('uploaded_at')
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'

        c = canvas.Canvas(response)
        c.drawString(50, 800, "Equipment Summary Report")

        y = 760
        for k, v in latest.summary.items():
            c.drawString(50, y, f"{k}: {v}")
            y -= 20

        c.save()
        return response
