import department
from department.models import Department, User
from gt_logs.models import GtLog
from manager.models import Manager
from django.db import models
from common.models import BaseModel
from  hod.models import Hod
from trainee.models import Trainee
# from accounts.models import User
########
from base64 import b32encode
from binascii import unhexlify
import time
from urllib.parse import quote, urlencode
from django.conf import settings
# from django_otp.oath import TOTP
# from django.db.models.constraints import UniqueConstraint





class ManagersComment(BaseModel):
    comment = models.TextField()
    manager = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='manager')
    approved = models.BooleanField(default=False)
    sent_for_approval = models.BooleanField(default=False)
    gt_score = models.IntegerField(default=0)
    trainee = models.ForeignKey(to = User, on_delete=models.CASCADE, null=True, related_name='trainee')
    department = models.ForeignKey(to = Department, on_delete=models.CASCADE, null=True, related_name='departments_managers_commnt')
    saved = models.BooleanField(default=False)


    


    def __str__(self):
        return f"{self.manager}'s comment on the log of: {self.trainee}"


class HodsComment(BaseModel):
    comment = models.TextField()
    hod = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='hod')
    hod_gt_score = models.IntegerField(default=0)
    managers_comment = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managers_comment')
    hod_gt_score = models.IntegerField(default=0)



    def __str__(self):
        return f"manager {self.managers_comment.name}'s comment on : Trainees Log"



class CommentTrail(BaseModel):
    comment = models.TextField()
    manager = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='manager_comment', null=True)
    trainee = models.ForeignKey(to = User, on_delete=models.CASCADE, null=True, related_name='trainee_commented_on')
           


class TraineeScore(BaseModel):
    trainee = models.ForeignKey(to = User, on_delete=models.CASCADE, null=True, related_name='trainee_scored')
    manager = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='manager_who_scored', null=True)
    number_comments = models.IntegerField(default=0)
    aggregate_score = models.IntegerField(default=0)
    attainable_score = models.IntegerField(default=0)
    department = models.ForeignKey(to=Department, on_delete=models.CASCADE, null=True, related_name='trainee_commented_on_department')

    def __str__(self):
        return f"manager {self.trainee.name}'s aggregate_score"



 