# Generated by Django 3.1.7 on 2021-03-16 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='mailbox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('first_name', models.CharField(max_length=40)),
                ('category', models.CharField(default='Employee', max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='mail_address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=60)),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailsapp1.mailbox')),
            ],
        ),
        migrations.CreateModel(
            name='mail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail_date', models.DateField()),
                ('previous_mail', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous_mail_id', to='mailsapp1.mail')),
                ('recipient_mail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient_mail_id', to='mailsapp1.mail_address')),
                ('response_mail', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='response_mail_id', to='mailsapp1.mail')),
                ('sender_mail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_mail_id', to='mailsapp1.mail_address')),
            ],
        ),
    ]
