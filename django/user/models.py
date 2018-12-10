from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in


class Profile(models.Model):
    # Field for the Dom Rep identification card (commonly known)
    # as 'cedula'. Must have exactly 11 digits
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, primary_key=True)
    id_card = models.CharField(validators=[RegexValidator(
        regex='^[0-9]{11}$',
        message='La cedula debe contener exactamente 11 digitos',
        code='nomatch')],
        max_length=11,
        blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(validators=[RegexValidator(
        regex='^(809|829|849)[0-9]{7}$',
        message='Debe ser un numero dominicano de 10 digitos',
        code='nomatch')],
        max_length=10,
        blank=True)

    MALE = 0
    FEMALE = 1
    GENDERS = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    gender = models.IntegerField(choices=GENDERS, default=MALE)

    def get_age(self):
        return timezone.now().year - self.birth_date.year

    def __str__(self):
        return f'{self.user}'

    # The following two methods are for when an user is created, automatically
    # fire the creation of the Profile model, saving all the related user info.
    @receiver(post_save, sender=get_user_model())
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=get_user_model())
    def save_user_profile(sender, instance, **kwargs):
        if not instance.is_superuser:
            instance.profile.save()


class SecurityQuestion(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.profile.__str__()} - {self.question} '

    class Meta:
        unique_together = ('question', 'profile')


class LoginLog(models.Model):
    profile = models.ForeignKey(
        'Profile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=30)
    user_agent = models.CharField(max_length=150, blank=True)
    locale = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f'{self.profile.user} | {self.timestamp}'

    @receiver(user_logged_in)
    def logged_in(sender, user, request, **kwargs):
        if not user.is_superuser:
            LoginLog.objects.create(
                profile=user.profile,
                ip=request.META['REMOTE_ADDR'],
                user_agent=request.META['HTTP_USER_AGENT'],
                locale=request.META['LC_IDENTIFICATION'])
