# Generated by Django 4.0.2 on 2022-02-14 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NBA', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='status_code',
        ),
    ]
