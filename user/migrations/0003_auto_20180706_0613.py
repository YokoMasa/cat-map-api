# Generated by Django 2.0.6 on 2018-07-06 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_sns_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
        migrations.RemoveField(
            model_name='user',
            name='password_digest',
        ),
    ]