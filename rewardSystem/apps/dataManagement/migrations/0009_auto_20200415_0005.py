# Generated by Django 2.2 on 2020-04-15 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataManagement', '0008_remove_jury_all_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='jury',
        ),
        migrations.AddField(
            model_name='jury',
            name='all_status',
            field=models.CharField(choices=[('未提交', '未提交'), ('已提交', '已提交')], default='未提交', max_length=3, verbose_name='全部是否提交'),
        ),
        migrations.AddField(
            model_name='jury',
            name='meeting',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='meeting_jury', to='dataManagement.Meeting', verbose_name='会议'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jury',
            name='user_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='用户id'),
        ),
    ]
