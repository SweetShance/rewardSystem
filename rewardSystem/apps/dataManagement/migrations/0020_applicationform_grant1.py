# Generated by Django 2.2 on 2020-04-16 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataManagement', '0019_auto_20200416_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationform',
            name='grant1',
            field=models.CharField(choices=[('研究生国家奖学金', '研究生国家奖学金'), ('研究生自治区奖学金', '研究生自治区奖学金'), ('研究生学校奖学金', '研究生学校奖学金')], max_length=20, null=True, verbose_name='国家级/自治区/学校级奖学金'),
        ),
    ]
