# Generated by Django 2.2.10 on 2021-04-16 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20210416_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail_address',
            name='box',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.mailbox'),
        ),
    ]