from django.db import models
from common.models import BaseModel
from department.models import Department, DepartmentHod, DepartmentManager

from accounts.models import User
import numbers_of_days

# from django.contrib.auth import get_user_model
# User = get_user_model()


class NumbersOfDays(BaseModel):


    # pending_all_approvals = 'pending approval'
    # sent_for_managers_approval = 'sent to manager'
    # sent_for_hods_approval = 'sent to hod'
    # approved_by_hod = 'approved by hod'
    # disapproved_by_hod = 'disapproved by hod'
   

    # numbers_of_days_status = [
    #    (pending_all_approvals, ('pending all approvals')),
    #    (sent_for_managers_approval, ('sent for managers approval')),
    #    (sent_for_hods_approval, ('sent for hods approval')),
    #    (approved_by_hod, ('approved by hod')),
    #    (disapproved_by_hod, ('disapproved by hod')),
    # ]


    numbers_of_days_status = (                          #private attributes
          ('pending_all_approvals', 'pending all approvals'),         
          ('sent_for_managers_approval', 'sent for managers approval'),
          ('sent_for_hods_approval', 'sent for hods approval'),
          ('approved_by_hod', 'approved by hod'),
          ('disapproved_by_hod', 'disapproved by hod'),
    )

    value = models.IntegerField(default=0)
    department = models.ForeignKey(to =Department, on_delete=models.CASCADE, null=True, related_name='departments_number_of_days')

    manager = models.ForeignKey(to=DepartmentManager, on_delete=models.CASCADE, null=True, blank=True, related_name='managers_numbers_of_days')
    hod = models.ForeignKey(to=DepartmentHod, on_delete=models.CASCADE, null=True, blank=True, related_name='hods_numbers_of_days')
    
    trainee = models.ForeignKey(to =User, on_delete=models.CASCADE, null=True, related_name='my_number_of_days')

    approved = models.BooleanField(default=False)
    managers_overall_comment = models.TextField(null=True, blank=True)
    numbers_of_days  = models.CharField(max_length=100, choices= numbers_of_days_status, null=True, default='pending_all_approvals')

    hods_overall_comment = models.TextField(null=True, blank=True)
    managers_overall_score = models.IntegerField(default=0)
    hods_overall_score = models.IntegerField(default=0)
    main_department = models.BooleanField(default=False)




    def __str__(self):
        return f"{self.trainee.name}: {self.department.department_name} department: {self.value} days"
        # return f"{self.department.department_name}"
