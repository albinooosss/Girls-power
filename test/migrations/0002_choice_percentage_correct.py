# Generated by Django 4.2.5 on 2024-07-10 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='percentage_correct',
            field=models.IntegerField(default=-1),
        ),
    ]
