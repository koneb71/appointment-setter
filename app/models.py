import datetime

import shortuuid as shortuuid
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

APPOINTMENT_STATUSES = dict(
    PENDING=0,
    PAID=1,
    CANCELLED=2,
)


class AdminUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class AdminUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(verbose_name='first name', max_length=100)
    last_name = models.CharField(verbose_name='last name', max_length=100)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = AdminUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DateTimeSlot(BaseModel):
    appointment_date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()
    status = models.SmallIntegerField(default=0)

    class Meta:
        unique_together = ('appointment_date', 'start', 'end')
        verbose_name = 'Time Slot'
        verbose_name_plural = 'Time Slots'

    def __str__(self):
        return f"{self.appointment_date.strftime('%Y-%m-%d')}: {self.start} - {self.end}"


class Appointment(BaseModel):
    reference_number = models.CharField(max_length=100, unique=True)
    slot = models.ForeignKey(DateTimeSlot, on_delete=models.DO_NOTHING)
    full_name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
    patient_type = models.CharField(max_length=10)
    status = models.SmallIntegerField(default=APPOINTMENT_STATUSES['PENDING'])

    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'

    def __str__(self):
        return f"{self.reference_number} - {self.full_name}"

    def save(self, *args, **kwargs):
        total_count = DateTimeSlot.objects.filter(appointment_date=self.slot.appointment_date).count()
        self.reference_number = f"{self.slot.appointment_date.strftime('%Y%m%d')}-{total_count+1}"
        slot = DateTimeSlot.objects.get(id=self.slot.id)
        slot.status = 1
        slot.save()

        super(Appointment, self).save(*args, **kwargs)