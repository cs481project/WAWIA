# Generated by Django 2.0.2 on 2018-02-28 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pollingSite', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='lastname',
            field=models.CharField(default='smith', max_length=128),
        ),
        migrations.AlterField(
            model_name='poll',
            name='correct',
            field=models.IntegerField(default=0),
        ),
    ]
