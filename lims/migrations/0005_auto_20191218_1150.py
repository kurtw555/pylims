# Generated by Django 2.2.5 on 2019-12-18 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0004_workflow_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='processor',
            name='enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='workflow',
            name='output_path',
            field=models.CharField(default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='processor',
            name='description',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='input_path',
            field=models.CharField(max_length=250),
        ),
    ]