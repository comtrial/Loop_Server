from django.db import models
from django.conf import settings
from group_api.models import Group
from feed_api.models import Feed


class Reports(models.Model):

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    object_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'user', on_delete=models.CASCADE, null=True)
    object_feed = models.ForeignKey(Feed, on_delete=models.CASCADE, null=True)
    object_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.reporter
