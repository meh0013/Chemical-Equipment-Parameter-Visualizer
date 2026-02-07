from django.urls import path
from .views import UploadCSVView, HistoryView, PDFView

urlpatterns = [
    path('upload/',UploadCSVView.as_view()),
    path('history/',HistoryView.as_view()),
    path("pdf/", PDFView.as_view()),
]
