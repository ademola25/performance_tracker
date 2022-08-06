from multiprocessing import managers
from django.db import models
from hod.models import Hod
from manager.models import Manager
from common.models import BaseModel

from django.contrib.auth import get_user_model


User = get_user_model()
class Department(BaseModel):
    department_name = models.CharField(max_length=150, null=True, blank=True, unique = True)
    key_objective = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.department_name}"

        

class DepartmentKeyObjective(BaseModel):
    department =  models.ForeignKey(to=Department, on_delete=models.CASCADE, null=True, blank=True, related_name='keys_department')
    key_objective = models.TextField(null=True, blank=True)
         


    def __str__(self):
        return f"{self.department} department: {self.key_objective}"


class DepartmentHod(BaseModel):
    department = models.ForeignKey(to=Department, on_delete=models.CASCADE, null=True, blank=True, related_name='department_departmenthod')
    hod = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True, related_name='hod_departmenthod')
    
    def __str__(self):
        return f"{self.department} HOD- {self.hod}"

  
class DepartmentTrainee(BaseModel):
    department = models.ForeignKey(to=Department, on_delete=models.CASCADE, null=True, blank=True, related_name='department_departmenttrainees')
    trainee = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True, related_name='trainee_departmenttrainees')
    
    def __str__(self):
        # return f"{self.trainee} trainee--- {self.department} department"
        return f"{self.department}"

        

class DepartmentManager(BaseModel):
    department = models.ForeignKey(to=Department, on_delete=models.CASCADE, null=True, blank=True, related_name='department_departmentmanagers')
    manager = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True, related_name='manager_departmentmanagers')
   

    def __str__(self):
        return f"Department Managers: {self.manager} {self.department}"