from django.db import models
from common.models import BaseModel
import department
from department.models import Department, DepartmentKeyObjective, User
from numbers_of_days.models import NumbersOfDays
from trainee.models import Trainee
# from comments.models import ManagersComment
from accounts.models import User
from django.utils import timezone



 
class GtLog(BaseModel):
    log = models.TextField()
    log_day = models.IntegerField(default=0)
    trainee = models.ForeignKey(to =User , on_delete=models.CASCADE, null=True, blank=True)
    number_of_days = models.ForeignKey(to=NumbersOfDays, on_delete=models.CASCADE,  null=True)
    saved = models.BooleanField(default=False)
    log_date = models.DateTimeField(default=timezone.now, null=True)
    kpi = models.ForeignKey(to=DepartmentKeyObjective,  on_delete=models.CASCADE, null=True, related_name='kpi_logs')
    department = models.ForeignKey(to = Department, on_delete=models.CASCADE,  null=True, related_name='department_gtlog' )
    def __str__(self):
        return f"{self.trainee}'s log for day: {self.log_day} of {self.number_of_days}"





