# Generated by Django 2.2.10 on 2021-04-15 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210415_1600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mail',
            name='next_mail',
        ),
        migrations.AddField(
            model_name='mail',
            name='next_mail',
            field=models.ManyToManyField(null=True, related_name='_mail_next_mail_+', to='app.mail'),
        ),
        migrations.RemoveField(
            model_name='mail',
            name='recipient_mail',
        ),
        migrations.AddField(
            model_name='mail',
            name='recipient_mail',
            field=models.ManyToManyField(null=True, related_name='recipient_mail_id', to='app.mail_address'),
        ),
    ]