# Generated by Django 4.2.3 on 2023-10-31 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0026_alter_question_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
