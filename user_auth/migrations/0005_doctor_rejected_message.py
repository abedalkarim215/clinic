# Generated by Django 3.2.2 on 2022-06-14 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0004_alter_education_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='rejected_message',
            field=models.TextField(blank=True, null=True),
        ),
    ]
