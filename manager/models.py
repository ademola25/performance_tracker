from django.db import models
from common.models import BaseModel



class Manager(BaseModel):
    manager_id = models.CharField(max_length=100, null=True, blank=True)
    manager_name = models.CharField(max_length=150, null=True, blank=True)
    manager_email = models.EmailField(max_length=150, null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.manager_id}: {self.manager_name}"
