# Generated by Django 2.0.6 on 2018-06-19 02:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0003_auto_20180611_1021'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw_image', models.ImageField(upload_to='cats/')),
                ('thumbnail', models.ImageField(upload_to='cats/')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cat.Cat')),
            ],
        ),
    ]
