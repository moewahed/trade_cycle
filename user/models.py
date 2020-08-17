from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, UnicodeUsernameValidator
)
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail

from .model_addon import UploadToPathAndRename


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )

        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')

        return self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            **extra_fields
        )


# class User(models.Model):
class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()
    # Email Field
    email = models.EmailField(
        verbose_name='Email',
        max_length=60,
        unique=True,
        help_text='Enter valid email: e.g. example@domain.com'
    )
    # Username Field
    username = models.CharField(
        verbose_name='Username',
        max_length=30,
        unique=True,
        validators=[username_validator],
        error_messages={'unique': "A user with that username already exists.", },
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. e.g. Mark99'
    )
    first_name = models.CharField(
        verbose_name='First Name',
        default=None,
        blank=True,
        null=True,
        max_length=255,
    )
    last_name = models.CharField(
        verbose_name='Last Name',
        default=None,
        blank=True,
        null=True,
        max_length=255,
    )
    birthday = models.DateField(
        verbose_name='Birthday',
        default=None,
        blank=True,
        null=True,
    )
    phone_no = models.CharField(
        verbose_name='Phone No.',
        default=None,
        blank=True,
        null=True,
        max_length=255,
        help_text='Your phone number started with the country code ex: +1'
    )
    address = models.CharField(
        verbose_name='Address',
        default=None,
        blank=True,
        null=True,
        max_length=255,
        help_text='City/State Can have both, separated by a comma.'
    )
    # Data Join, auto add upon the date that created at
    date_joined = models.DateTimeField(
        verbose_name='join date',
        auto_now_add=True
    )
    # Data Join, auto add upon the date that update at
    last_login = models.DateTimeField(
        verbose_name='last login',
        auto_now=True
    )

    # Boolean Fields for the authentication and the activation, default value is provided for each one
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    profile_pic = models.ImageField(
        verbose_name='Profile Image',
        default='default/img/profile.png',
        upload_to=UploadToPathAndRename('upload/img/profile'),
        validators=[
            FileExtensionValidator(['png', 'jpg', 'jpeg']),
        ],
        help_text='Limits:<ul><li>Size 2MB</li><li>Dimensions Range: Width & height (200-1600)</li></ul>'
    )
    cover_pic = models.ImageField(
        verbose_name='Cover Image',
        default='default/img/cover.png',
        upload_to=UploadToPathAndRename('upload/img/cover'),
        validators=[
            FileExtensionValidator(['png', 'jpg', 'jpeg', 'PNG', 'JPG']),
        ],
        help_text='Limits:<ul><li>Size 4MB</li><li>Dimensions Range: Width & height (400-2600)</li></ul>',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = MyUserManager()

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return ('%s' % self.username).strip()

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return ('%s %s' % (self.first_name, self.last_name)).strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return ('%s' % self.first_name).strip()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
