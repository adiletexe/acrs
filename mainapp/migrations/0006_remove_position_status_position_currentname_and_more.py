# Generated by Django 4.2.1 on 2023-08-22 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_position_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='position',
            name='status',
        ),
        migrations.AddField(
            model_name='position',
            name='currentname',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='position',
            name='steps_left',
            field=models.IntegerField(blank=True, default=20),
            preserve_default=False,
        ),
    ]
