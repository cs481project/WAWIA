# Generated by Django 2.0.1 on 2018-02-19 21:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pollingSite', '0007_classroom_classkey'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='classKey',
        ),
    ]
