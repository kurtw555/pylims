# Generated by Django 2.2.5 on 2020-01-15 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0007_auto_20200115_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='processor',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
