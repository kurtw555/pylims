# Generated by Django 2.2.5 on 2020-01-16 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0009_auto_20200115_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processor',
            name='name',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='processor_name',
            field=models.CharField(default='', max_length=40),
        ),
    ]