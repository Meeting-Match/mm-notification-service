from django.db import models

# Create your models here.


class Notification(models.Model):
    NotificationID = models.AutoField(primary_key=True)
    Message = models.CharField(max_length=255)
    SentStatus = models.BooleanField(default=False)
    CreatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Message

