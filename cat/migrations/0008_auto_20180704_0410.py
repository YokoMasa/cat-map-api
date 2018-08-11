# Generated by Django 2.0.6 on 2018-07-04 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '__first__'),
        ('cat', '0007_auto_20180626_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cat',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]