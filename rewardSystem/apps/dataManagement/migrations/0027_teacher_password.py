# Generated by Django 2.2 on 2020-04-17 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataManagement', '0026_auto_20200416_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='password',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='密码'),
        ),
    ]
