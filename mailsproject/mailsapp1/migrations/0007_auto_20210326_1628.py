# Generated by Django 3.1.7 on 2021-03-26 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailsapp1', '0006_auto_20210326_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='previous_mail',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='mailsapp1.mail'),
        ),
        migrations.AlterField(
            model_name='mail',
            name='response_mail',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='mailsapp1.mail'),
        ),
    ]
