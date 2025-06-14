# Generated by Django 5.2.1 on 2025-06-02 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fly', '0004_auto_20250602_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='is_coach',
            field=models.BooleanField(default=False, verbose_name='是否教员'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='删除状态'),
        ),
        migrations.AlterField(
            model_name='operatingbase',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='删除状态'),
        ),
        migrations.AlterField(
            model_name='operatingbase',
            name='status',
            field=models.SmallIntegerField(choices=[(1, '启用'), (2, '停用')], default=1, verbose_name='状态'),
        ),
    ]
