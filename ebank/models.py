from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class UserModelManager(UserManager):
    """Extends UserManager
    
    This ensures that CaSe InsenSItiVE usernames are recognized as one."""

    def get_by_natural_key(self, username):
        """Enable caSE insiSITive username look up."""
        case_insensitive_username = f'{self.model.USERNAME_FIELD}__iexact'
        return self.get(**{case_insensitive_username: username})


class User(AbstractUser):
    """Extends AbstractUser

    Defines one extra required field to help with user registration and
    verification."""

    email_verified = models.BooleanField(
        help_text="Is user email verified?", default=False
    )

    objects = UserModelManager()


class Profile(models.Model):
    """Holds other user details.

    Adds more fields to the user object by linking through One To One
    relationship.

    This model is just a basic extention of the Default User model.
    """

    ACCOUNT_TYPES = (
        ('A', 'Agent'),
        ('C', 'Core Team'),
        ('R', 'Regular'),
    )

    GENDERS = (
        ("M", "Male"),
        ("F", "Female"),
        ("T", "Transgender"),
        ("O", "Other"),
    )

    STATUSES = (
        ("M", "Married"),
        ("S", "Single"),
        ("E", "Engaged"),
        ("D", "Divorced"),
        ("O", "Others"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='profile', help_text='More user data'
    )
    other_name = models.CharField(
        max_length=50, blank=True, help_text='Other names'
    )
    account_type = models.CharField(
        max_length=2, choices=ACCOUNT_TYPES, default='R',
        help_text='What is the account type?'
    )
    gender = models.CharField(
        max_length=2, choices=GENDERS, blank=True, help_text='Gender'
    )
    status = models.CharField(
        max_length=2, choices=STATUSES, blank=True, help_text='Marital status'
    )
    phone = models.CharField(
        max_length=14, blank=True, default='+2340123456789',
        help_text='Mobile number'
    )
    address = models.CharField(
        max_length=150, blank=True, help_text='Contact address'
    )
    passport = models.ImageField(
        upload_to='passports', blank=True, help_text='Profile picture'
    )
    modified = models.DateTimeField(auto_now=True, help_text='Last modifield')

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        """Return URL to user profile depending on account type."""
        if self.account_type == 'C':
            return reverse('home')  # Will redirect to Core Dashboard later
        elif self.account_type == 'A':
            return reverse('home')  # Will redirect to Agent Dashboard later
        return reverse('home')  # Will redirect to Customer Dashboard later

    def full_name(self):
        """Returns the user's full name."""
        return self.user.get_full_name() + self.other_name or \
            self.user.username

    def get_alternate_avatar(self):
        """Returns text to use as avatar when user avatar is not available.

        This method should only be called as alternative to get_avatar()."""
        try:
            pic = f'{self.user.first_name[0]} {self.user.last_name[0]}'
            return pic.upper()
        except IndexError:
            return self.user.username[:2].upper()


class Transfer(models.Model):
    """Keeps record of each transfer."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        help_text='User transferring', null=True
    )
    account = models.IntegerField(
        help_text='Account number to be tranfer to',
    )
    amount = models.DecimalField(
        max_digits=9, decimal_places=2, help_text='Amount to transfer'
    )
    note = models.CharField(
        max_length=255, blank=True, default='Transfer',
        help_text='Provide optional note/description'
    )
    date = models.DateTimeField(
        auto_now_add=True, help_text='Transaction date and time'
    )

    def __str__(self):
        return f'Transferred {self.amount} to {self.account}'


class TempTransfer(models.Model):
    """Keeps record of each initialized transfer."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        help_text='User transferring', null=True
    )
    account = models.IntegerField(
        help_text='Account number to be tranfer to',
    )
    amount = models.DecimalField(
        max_digits=9, decimal_places=2, help_text='Amount to transfer'
    )
    token = models.IntegerField(help_text='Six digit Bank Token', unique=True)
    note = models.CharField(
        max_length=255, blank=True, default='Transfer',
        help_text='Provide optional note/description'
    )
    date = models.DateTimeField(
        auto_now_add=True, help_text='Transaction date and time'
    )

    def __str__(self):
        return f'Waiting transfer to {self.account}'


class Withdraw(models.Model):
    """Keeps record of each withdrawal."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, help_text='User withdrawing'
    )
    account = models.IntegerField(help_text='From which account?')
    amount = models.DecimalField(
        max_digits=9, decimal_places=2, help_text='Amount to withdraw'
    )
    note = models.CharField(
        max_length=255, blank=True, default='Withdrawal',
        help_text='Provide optional note/description'
    )
    date = models.DateTimeField(
        auto_now_add=True, help_text='Transaction date and time'
    )

    def __str__(self):
        return f'Withdrew {self.amount} from {self.account}'


class Deposit(models.Model):
    """Keeps record of each deposit."""

    user = models.CharField(max_length=100, help_text='User depositing')
    account = models.IntegerField(help_text='Into which account?',)
    amount = models.DecimalField(
        max_digits=9, decimal_places=2, help_text='Amount to deposit'
    )
    note = models.CharField(
        max_length=255, blank=True, default='Deposit',
        help_text='Provide optional note/description'
    )
    date = models.DateTimeField(
        auto_now_add=True, help_text='Transaction date and time'
    )

    def __str__(self):
        return f'Deposited {self.amount} into {self.account}'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """This signal listens for when new user is created and creates
    corresponding profile."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """Automatically updates user profile each time the user instance is
    saved."""
    instance.profile.save()
