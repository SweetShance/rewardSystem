# Generated by Django 2.2 on 2020-04-14 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataManagement', '0003_auto_20200414_1721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jury',
            name='chief_umpire_status',
        ),
    ]
