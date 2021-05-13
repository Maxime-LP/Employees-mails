# Generated by Django 2.2.10 on 2021-05-13 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('enron_id', models.CharField(max_length=120, primary_key=True, serialize=False)),
                ('date', models.DateTimeField(null=True)),
                ('subject', models.CharField(max_length=200, null=True)),
                ('isReply', models.BooleanField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='mailAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.EmailField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('inEnron', models.BooleanField()),
                ('category', models.CharField(max_length=40, null=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(fields=('name',), name='name_unique'),
        ),
        migrations.AddField(
            model_name='mailaddress',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.User'),
        ),
        migrations.AddField(
            model_name='mail',
            name='recipient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to='app.mailAddress'),
        ),
        migrations.AddField(
            model_name='mail',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='app.mailAddress'),
        ),
        migrations.AddConstraint(
            model_name='mailaddress',
            constraint=models.UniqueConstraint(fields=('address',), name='address_unique'),
        ),
    ]
