# Generated by Django 2.2.5 on 2019-12-11 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims', '0003_auto_20191211_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='workflow',
            name='name',
            field=models.CharField(default='', max_length=20),
        ),
    ]