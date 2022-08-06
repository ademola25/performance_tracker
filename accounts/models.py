from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from common .models import BaseModel
from hr_personnel.models import Batch



from django_otp.util import hex_validator, random_hex
from base64 import b32encode
from binascii import unhexlify
from django_otp.oath import TOTP
import time
from urllib.parse import quote, urlencode
from django.conf import settings

 


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Email cannot be blank.')
        
        # if not password:
        #     raise ValueError('Password cannot be blank.')
        
        user = self.model(
            email= self.normalize_email(email),
        )

        import random
        import string
        letters = string.ascii_lowercase
        user.set_password(''.join(random.choice(letters) for i in range(10)) )
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        user  = self.create_user(email)
        user.staff = True
        user.set_password(password)
        user = user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email)
        user.staff = True
        user.admin = True
        user.set_password(password)
        user = user.save(using=self._db)
        return user
    

class User(BaseModel ,AbstractBaseUser):

    account_roles = (                          #private attributes
          ('hr', 'Hr'),
          ('trainee', 'Trainee'),
          ('hod', 'Hod'),
          ('manager', 'Manager'),          
    )
    role  = models.CharField(max_length=100, choices= account_roles, null=True)
    has_password = models.BooleanField(default=False)
    batch = models.ForeignKey(Batch, null=True,blank=True, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=300, null=True, blank=True)
    name = models.CharField(max_length=300, null=True, blank=True)
    email = models.EmailField(max_length=250, unique=True)
    admin = models.BooleanField(default=False)

    staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    workforce = models.ManyToManyField("Workforce", related_name="user_workforce")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f'{self.email}'

    def has_perm(self, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    def get_fullname(self):
        return self.email

    def get_shortname(self):
        return self.email.split('@')[0]

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

class Workforce(BaseModel):
    choice_roles = (                          #private attributes
          ('sales', 'Sales'),
          ('operations', 'Operations'),         
    )
    name = models.CharField(max_length=30, choices=choice_roles, unique=True)
    def __str__(self):
        return f"{self.name}"

    



def default_key():
    return random_hex(20)


def key_validator(value):
    return hex_validator()(value)


class TOTPDevice(BaseModel):
    key = models.CharField(max_length=80, validators=[
                           key_validator], default=default_key,
                           help_text="A hex-encoded secret key of up to 40 bytes.")
    step = models.PositiveSmallIntegerField(default=30, help_text="The time step in seconds.")
    t0 = models.BigIntegerField(
        default=0, help_text="The Unix time at which to begin counting steps.")
    digits = models.PositiveSmallIntegerField(
        choices=[(6, 6), (8, 8)], default=6, help_text="The number of digits to expect in a token.")
    tolerance = models.PositiveSmallIntegerField(
        default=1, help_text="The number of time steps in the past or future to allow.")
    drift = models.SmallIntegerField(
        default=0, help_text="The number of time steps the prover is known to deviate from clock.")
    last_t = models.BigIntegerField(
        default=-1,
        help_text="The t value of the latest verified token.")

    @property
    def bin_key(self):
        """
        The secret key as a binary string.
        """
        return unhexlify(self.key.encode())

    def verify_token(self, token):
        OTP_TOTP_SYNC = True
        try:
            token = int(token)
        except Exception:
            verified = False
        else:
            key = self.bin_key

            totp = TOTP(key, self.step, self.t0, self.digits, self.drift)
            totp.time = time.time()

            verified = totp.verify(token, self.tolerance, self.last_t + 1)
            if verified:
                self.last_t = totp.t()
                if OTP_TOTP_SYNC:
                    self.drift = totp.drift
                self.save()
        return verified


class UserTOTPDevice(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='totp_device')
    name = models.CharField(max_length=64, default='HCM 2FA',
                            help_text="The human-readable name of this device.")
    confirmed = models.BooleanField(default=False, help_text="Is this device ready for use?")
    device = models.OneToOneField(TOTPDevice, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_fullname()

    @property
    def config_url(self):
        label = self.user.get_shortname()
        params = {
            'secret': b32encode(self.device.bin_key),
            'algorithm': 'SHA1',
            'digits': self.device.digits,
            'period': self.device.step,
        }
        urlencoded_params = urlencode(params)

        issuer = getattr(settings, 'OTP_TOTP_ISSUER', None)
        if callable(issuer):
            issuer = issuer(self)
        if isinstance(issuer, str) and (issuer != ''):
            issuer = issuer.replace(':', '')
            label = '{}:{}'.format(issuer, label)
            # encode issuer as per RFC 3986, not quote_plus
            urlencoded_params += '&issuer={}'.format(quote(issuer))

        url = 'otpauth://totp/{}?{}'.format(quote(label), urlencoded_params)

        return url

