# Generated by Django 4.2.5 on 2024-07-10 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test', '0004_result_choice_set_alter_result_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='result',
            unique_together=set(),
        ),
    ]
