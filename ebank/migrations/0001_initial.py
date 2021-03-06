# Generated by Django 3.1.1 on 2020-09-30 15:11

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import ebank.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email_verified', models.BooleanField(default=False, help_text='Is user email verified?')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', ebank.models.UserModelManager()),
            ],
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(help_text='User depositing', max_length=100)),
                ('account', models.BigIntegerField(help_text='Into which account?')),
                ('amount', models.DecimalField(decimal_places=2, help_text='Amount to deposit', max_digits=9)),
                ('note', models.CharField(blank=True, default='Deposit', help_text='Provide optional note/description', max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True, help_text='Transaction date and time')),
            ],
        ),
        migrations.CreateModel(
            name='Withdraw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.BigIntegerField(help_text='From which account?')),
                ('amount', models.DecimalField(decimal_places=2, help_text='Amount to withdraw', max_digits=9)),
                ('note', models.CharField(blank=True, default='Withdrawal', help_text='Provide optional note/description', max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True, help_text='Transaction date and time')),
                ('user', models.ForeignKey(help_text='User withdrawing', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.BigIntegerField(help_text='Account number to be tranfer to')),
                ('amount', models.DecimalField(decimal_places=2, help_text='Amount to transfer', max_digits=9)),
                ('note', models.CharField(blank=True, default='Transfer', help_text='Provide optional note/description', max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True, help_text='Transaction date and time')),
                ('user', models.ForeignKey(help_text='User transferring', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TempTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.BigIntegerField(help_text='Account number to be tranfer to')),
                ('amount', models.DecimalField(decimal_places=2, help_text='Amount to transfer', max_digits=9)),
                ('token', models.IntegerField(help_text='Six digit Bank Token', unique=True)),
                ('note', models.CharField(blank=True, default='Transfer', help_text='Provide optional note/description', max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True, help_text='Transaction date and time')),
                ('user', models.ForeignKey(help_text='User transferring', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('other_name', models.CharField(blank=True, help_text='Other names', max_length=50)),
                ('account_type', models.CharField(choices=[('A', 'Agent'), ('C', 'Core Team'), ('R', 'Regular')], default='R', help_text='What is the account type?', max_length=2)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('T', 'Transgender'), ('O', 'Other')], help_text='Gender', max_length=2)),
                ('status', models.CharField(blank=True, choices=[('M', 'Married'), ('S', 'Single'), ('E', 'Engaged'), ('D', 'Divorced'), ('O', 'Others')], help_text='Marital status', max_length=2)),
                ('phone', models.CharField(blank=True, help_text='Mobile number', max_length=14)),
                ('address', models.CharField(blank=True, help_text='Contact address', max_length=150)),
                ('passport', models.ImageField(blank=True, help_text='Profile picture', upload_to='passports')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Last modifield')),
                ('user', models.OneToOneField(help_text='More user data', on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
