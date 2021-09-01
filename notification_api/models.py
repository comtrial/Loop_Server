from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Notification(models.Model) :

    NOTIFICATION_TYPES = (
        ('group', 'group'),
        ('comment', 'comment')
    )
        
    
    # id = models.AutoField(db_column='id', primary_key=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='to')
    target_idx = models.IntegerField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)

    # def __str__(self):
    #     return self.author