from django.db import models


# Create your models here.
class ReportData(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(default=0)
    user_id = models.BigIntegerField(null=True, blank=True)
    
    def __str__(self):
        return self.name or "no name"
