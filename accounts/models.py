import random
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from shared.models import BaseModel
from datetime import datetime, timedelta
import uuid

VIA_EMAIL, VIA_PHONE = 'via_email', 'via_phone'

AUTH_TYPE = (
    (VIA_EMAIL, "Via Email"),
    (VIA_PHONE, "Via Phone"),
)

EXPIRATION_PHONE = 2  #
EXPIRATION_EMAIL = 5


class CustomUser(BaseModel, AbstractUser):
    auth_type = models.CharField(max_length=31, choices=AUTH_TYPE)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=13, unique=True, blank=True, null=True)


    def __str__(self):
        return self.username

    def create_verify_code(self, verify_type):
        if not self.pk:
            self.save()
        code = random.randint(1000, 9999)
        CodeVerified.objects.create(
            code=code,
            user=self,
            verify_type=verify_type
        )
        return code

    def check_username(self):
        if not self.username:
            self.username = f"ins{uuid.uuid4().__str__().split('-')[-1]}"
            while CustomUser.objects.filter(username=self.username).exists():
                self.username = f"{self.username}+{str(random.randint(0, 100))}"

    def check_email(self):
        if self.email:
            self.email = self.email.lower()

    def check_pass(self):
        if not self.password:
            self.password = f'password-{uuid.uuid4().__str__().split("-")[-1]}'

    def hashing_pass(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def token(self):
        token = RefreshToken.for_user(self)
        return {
            'refresh_token': str(token),
            'access_token': str(token.access_token)
        }

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        self.check_email()
        self.check_username()
        self.check_pass()
        self.hashing_pass()


class CodeVerified(BaseModel):
    code = models.CharField(max_length=4, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='verify_codes')
    verify_type = models.CharField(max_length=31, choices=AUTH_TYPE)
    expiration_time = models.DateTimeField()
    code_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.verify_type == VIA_EMAIL:
            self.expiration_time = datetime.now() + timedelta(minutes=EXPIRATION_EMAIL)
        else:
            self.expiration_time = datetime.now() + timedelta(minutes=EXPIRATION_PHONE)
        super().save(*args, **kwargs)
