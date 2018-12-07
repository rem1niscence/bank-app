from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser


class BankUser(AbstractBaseUser):
    # Field for the Dom Rep identification card (commonly known)
    # as 'cedula'. Must have exactly 11 digits
    id_card = models.CharField(validators=[RegexValidator(
        regex='^[0-9]{11}$',
        message='La cedula debe contener exactamente 11 digitos',
        code='nomatch')],
        unique=True,
        max_length=11)
    date_of_birth = models.DateField()
