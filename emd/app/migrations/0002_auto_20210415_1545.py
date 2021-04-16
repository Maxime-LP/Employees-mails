# Generated by Django 2.2.10 on 2021-04-15 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mail',
            old_name='response_mail',
            new_name='next_mail',
        ),
        migrations.AddField(
            model_name='mail',
            name='mailbox',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='app.mailbox'),
        ),
        migrations.AddField(
            model_name='mail',
            name='subject',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='mail',
            name='mail_date',
            field=models.DateTimeField(null=True),
        ),
    ]