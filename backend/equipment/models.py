from django.db import models

class EquipmentDataset(models.Model):
    filename=models.CharField(max_length=255)
    uploaded_at=models.DateTimeField(auto_now_add=True)
    summary=models.JSONField()

    def __str__(self):
        return self.filename

class UploadHistory(models.Model):
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary = models.JSONField()

    def __str__(self):
        return f"{self.filename} ({self.uploaded_at})"

