# Generated by Django 2.2 on 2020-04-16 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataManagement', '0018_auto_20200416_0954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicationform',
            name='grant',
        ),
        migrations.RemoveField(
            model_name='applicationform',
            name='grant1',
        ),
        migrations.RemoveField(
            model_name='applicationform',
            name='grant2',
        ),
        migrations.RemoveField(
            model_name='applicationform',
            name='grant3',
        ),
    ]
