# Generated by Django 2.2.5 on 2020-01-15 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0008_auto_20200113_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workflow',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
