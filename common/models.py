from django.db import models
import uuid
from django_otp.util import hex_validator, random_hex
from base64 import b32encode
from binascii import unhexlify
from django_otp.oath import TOTP
import time

 

class BaseModel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True



