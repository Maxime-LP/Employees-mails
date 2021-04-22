# Generated by Django 2.2.10 on 2021-04-15 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20210415_1733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mail',
            name='next_mail',
        ),
        migrations.AddField(
            model_name='mail',
            name='next_mail',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='app.mail'),
        ),
        migrations.RemoveField(
            model_name='mail',
            name='recipient_mail',
        ),
        migrations.AddField(
            model_name='mail',
            name='recipient_mail',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipient_mail_id', to='app.mail_address'),
        ),
    ]
