from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Profile(models.Model):
    # Field for the Dom Rep identification card (commonly known)
    # as 'cedula'. Must have exactly 11 digits
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, primary_key=True)
    id_card = models.CharField(validators=[RegexValidator(
        regex='^[0-9]{11}$',
        message='La cedula debe contener exactamente 11 digitos',
        code='nomatch')],
        max_length=11)
    date_of_birth = models.DateField()
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(validators=[RegexValidator(
        regex='^(809|829|849)[0-9]{7}$',
        message='Debe ser un numero dominicano de 10 digitos',
        code='nomatch')],
        max_length=10)

    MALE = 0
    FEMALE = 1
    GENDERS = (
        (MALE, 'Hombre'),
        (FEMALE, 'Mujer'),
    )
    gender = models.IntegerField(choices=GENDERS, default=MALE)

    # The following two methods are for when an user is created, automatically
    # fire the creation of the Profile model, saving all the related user info.
    @receiver(post_save, sender=get_user_model())
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=get_user_model())
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def get_age(self):
        return timezone.now().year - self.date_of_birth.year

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class SecurityQuestion(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.__str__()} - {self.question} '

    class Meta:
        unique_together = ('question', 'user')
