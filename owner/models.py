from django.db import models

# Create your models here.
class OwnerDetails(models.Model):
    name = models.CharField(max_length=100)
    helpline_no = models.CharField(max_length=100, blank=True, null=True)
    office_address = models.CharField(max_length=1000, blank=True, null=True)