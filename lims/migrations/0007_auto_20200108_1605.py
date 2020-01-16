# Generated by Django 2.2.5 on 2020-01-08 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0006_workflow_processor_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflow',
            name='v_input_path',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workflow',
            name='v_output_path',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(default='PENDING', max_length=50),
        ),
    ]
