# Generated by Django 3.1.1 on 2020-09-30 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebank', '0003_auto_20200930_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, default='+2340123456789', help_text='Mobile number', max_length=14),
        ),
    ]