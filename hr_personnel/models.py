from turtle import mode
from django.db import models
from common.models import BaseModel
from django.core.validators import FileExtensionValidator

from django.utils.translation import gettext_lazy as _





class HrPersonnel(models.Model):
    hr_personnel_id = models.CharField(max_length=100, null=True, blank=True)
    hr_personnel_name = models.CharField(max_length=150, null=True, blank=True)
    hr_personnel_email = models.EmailField(max_length=150, null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.hr_personnel_id}: {self.hr_personnel_name}"



class Batch(models.Model):
    batch_name = models.CharField(max_length=100, null=True, blank=True)
    csv_file = models.FileField(upload_to='csv_files/')
    uploaded_by = models.CharField(max_length=150, null=True, blank=True)
    completed = models.BooleanField(default=False)
    month_year = models.DateTimeField(null=True, help_text='Start month and year of training')



    def __str__(self):
        return f"Batch Name: {self.batch_name}"



class HodCreationError(BaseModel):
    error_message = models.TextField(null=True, editable=False)
    batch = models.ForeignKey(Batch, null=True, blank=True, on_delete=models.CASCADE, related_name='batchs_error')

    def __str__(self):
        return f"Batch Name: {self.error_message}"