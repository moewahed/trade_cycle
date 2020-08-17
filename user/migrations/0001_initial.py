# Generated by Django 2.2 on 2020-08-14 00:24

import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(help_text='Enter valid email: e.g. example@domain.com', max_length=60, unique=True, verbose_name='Email')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only. e.g. Mark99', max_length=30, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='Username')),
                ('first_name', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Last Name')),
                ('birthday', models.DateField(blank=True, default=None, null=True, verbose_name='Birthday')),
                ('phone_no', models.CharField(blank=True, default=None, help_text='Your phone number started with the country code ex: +1', max_length=255, null=True, verbose_name='Phone No.')),
                ('address', models.CharField(blank=True, default=None, help_text='City/State Can have both, separated by a comma.', max_length=255, null=True, verbose_name='Address')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='join date')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('profile_pic', models.ImageField(default='static/default/img/profile.png', help_text='Limits:<ul><li>Size 2MB</li><li>Dimensions Range: Width & height (200-1600)</li></ul>', upload_to=user.models.UploadToPathAndRename('upload/img/profile'), validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])], verbose_name='Profile Image')),
                ('cover_pic', models.ImageField(default='static/default/img/cover.png', help_text='Limits:<ul><li>Size 4MB</li><li>Dimensions Range: Width & height (400-2600)</li></ul>', upload_to=user.models.UploadToPathAndRename('upload/img/cover'), validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'PNG', 'JPG'])], verbose_name='Cover Image')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'account',
                'verbose_name_plural': 'accounts',
            },
        ),
    ]
