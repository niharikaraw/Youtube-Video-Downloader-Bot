from django.db import models

# Create your models here.
class FileInfo(models.Model):
    video_name = models.TextField(null=True)
    video_id = models.CharField(max_length=255, null=True)
