# Generated by Django 3.0.3 on 2021-11-07 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quizz_project_app', '0009_auto_20211107_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='img_id',
            field=models.IntegerField(),
        ),
    ]
