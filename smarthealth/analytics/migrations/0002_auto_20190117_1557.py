# Generated by Django 2.1.5 on 2019-01-17 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='dob',
            field=models.DateTimeField(),
        ),
    ]