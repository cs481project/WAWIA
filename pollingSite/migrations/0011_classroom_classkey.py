# Generated by Django 2.0.1 on 2018-02-19 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pollingSite', '0010_remove_classroom_classkey'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='classKey',
            field=models.CharField(default='123456', max_length=6, unique=True),
            preserve_default=False,
        ),
    ]
