# Generated by Django 3.1.7 on 2021-03-15 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailsapp1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='mail_date',
            field=models.DateField(null=True),
        ),
    ]
