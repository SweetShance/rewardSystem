# Generated by Django 2.2 on 2020-04-16 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataManagement', '0016_auto_20200416_0930'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applicationform',
            old_name='grant',
            new_name='grant1',
        ),
        migrations.AddField(
            model_name='applicationform',
            name='grant2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grant2', to='dataManagement.GrantLevel', verbose_name='助学金'),
        ),
        migrations.AddField(
            model_name='applicationform',
            name='grant3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='grant3', to='dataManagement.GrantLevel', verbose_name='学业奖学金'),
        ),
    ]
