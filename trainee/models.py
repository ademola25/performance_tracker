from django.db import models
from common.models import BaseModel




class Trainee(BaseModel):
    trainee_id = models.CharField(max_length=100, null=True, blank=True)
    trainee_name = models.CharField(max_length=150, null=True, blank=True)
    trainee_email = models.EmailField(max_length=150, null=True, blank=True, unique=True)
    
    


    def __str__(self):
        return f"{self.trainee_id}: {self.trainee_name}"
