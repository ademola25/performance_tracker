from django.db import models
from common.models import BaseModel



class Hod(BaseModel):
    hod_id = models.CharField(max_length=100, null=True, blank=True)
    hod_name = models.CharField(max_length=150, null=True, blank=True)
    hod_email = models.EmailField(max_length=150, null=True, blank=True, unique=True)
    hod_gt_score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.hod_id}: {self.hod_name}"
