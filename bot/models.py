from django.db import models


# Create your models here.
class FileInfo(models.Model):
    video_name = models.TextField(null=True)
    video_id = models.CharField(max_length=255, unique=True, primary_key=True)


class CustomUser(models.Model):
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    chat_id = models.CharField(max_length=255, unique=True, primary_key=True)

class UserHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    video = models.ForeignKey(FileInfo, on_delete=models.CASCADE, null=True)
    date_requested = models.DateTimeField(auto_created=True)

