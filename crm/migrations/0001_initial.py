# Generated by Django 3.2.12 on 2022-02-02 10:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Circle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('desciption', models.TextField()),
                ('color', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Circle',
                'verbose_name_plural': 'Circles',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('logo', models.ImageField(upload_to='company/logo')),
                ('background_info', models.TextField()),
                ('phone', models.CharField(max_length=100)),
                ('webiste', models.URLField()),
                ('skype', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=50)),
                ('zip_code', models.IntegerField()),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='CompanyCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staus', models.IntegerField(choices=[(1, 'Active'), (2, 'Inactive')])),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Company Category',
                'verbose_name_plural': 'Company Categories',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.IntegerField(choices=[(1, 'Lead'), (2, 'Prospect'), (3, 'Client')])),
                ('name_prefix', models.CharField(max_length=4)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='contacts')),
                ('title', models.CharField(max_length=200)),
                ('background_info', models.TextField()),
                ('phone', models.CharField(max_length=100)),
                ('webiste', models.URLField()),
                ('skype', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=500)),
                ('city', models.CharField(max_length=50)),
                ('zip_code', models.IntegerField()),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.company')),
                ('coordinator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staus', models.IntegerField(choices=[(1, 'Active'), (2, 'Inactive')])),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Event Category',
                'verbose_name_plural': 'Event Categories',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visibility', models.IntegerField(choices=[(1, 'Public'), (2, 'Private')])),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('duration', models.CharField(choices=[('15 minutes', '15 minutes'), ('30 minutes', '30 minutes'), ('45 minutes', '45 minutes'), ('1 hour', '1 hour'), ('1 hour 15 minutes', '1 hour 15 minutes'), ('1 hour 30 minutes', '1 hour 30 minutes'), ('1 hour 45 minutes', '1 hour 45 minutes'), ('2 hour', '2 hour'), ('2 hours 15 minutes', '2 hours 15 minutes'), ('2 hours 30 minutes', '2 hours 30 minutes'), ('2 hours 45 minutes', '2 hours 45 minutes'), ('3 hour', '3 hour'), ('3 hours 15 minutes', '3 hours 15 minutes'), ('3 hours 30 minutes', '3 hours 30 minutes'), ('3 hours 45 minutes', '3 hours 45 minutes'), ('4 hour', '4 hour'), ('4 hours 15 minutes', '4 hours 15 minutes'), ('4 hours 30 minutes', '4 hours 30 minutes'), ('4 hours 45 minutes', '4 hours 45 minutes'), ('5 hour', '5 hour'), ('5 hours 15 minutes', '5 hours 15 minutes'), ('5 hours 30 minutes', '5 hours 30 minutes'), ('5 hours 45 minutes', '5 hours 45 minutes'), ('6 hour', '6 hour'), ('6 hours 15 minutes', '6 hours 15 minutes'), ('6 hours 30 minutes', '6 hours 30 minutes'), ('6 hours 45 minutes', '6 hours 45 minutes'), ('7 hour', '7 hour'), ('7 hours 15 minutes', '7 hours 15 minutes'), ('7 hours 30 minutes', '7 hours 30 minutes'), ('7 hours 45 minutes', '7 hours 45 minutes'), ('8 hour', '8 hour'), ('8 hours 15 minutes', '8 hours 15 minutes'), ('8 hours 30 minutes', '8 hours 30 minutes'), ('8 hours 45 minutes', '8 hours 45 minutes'), ('9 hour', '9 hour'), ('9 hours 15 minutes', '9 hours 15 minutes'), ('9 hours 30 minutes', '9 hours 30 minutes'), ('9 hours 45 minutes', '9 hours 45 minutes'), ('10 hour', '10 hour'), ('10 hours 15 minutes', '10 hours 15 minutes'), ('10 hours 30 minutes', '10 hours 30 minutes'), ('10 hours 45 minutes', '10 hours 45 minutes'), ('11 hour', '11 hour'), ('11 hours 15 minutes', '11 hours 15 minutes'), ('11 hours 30 minutes', '11 hours 30 minutes'), ('11 hours 45 minutes', '11 hours 45 minutes'), ('12 hour', '12 hour'), ('12 hours 15 minutes', '12 hours 15 minutes'), ('12 hours 30 minutes', '12 hours 30 minutes'), ('12 hours 45 minutes', '12 hours 45 minutes')], max_length=100)),
                ('description', models.TextField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.contact')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.AddField(
            model_name='company',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.companycategory'),
        ),
        migrations.CreateModel(
            name='CircleClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('circle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.circle')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.contact')),
            ],
            options={
                'verbose_name': 'Circle Client',
                'verbose_name_plural': 'Circle Clients',
            },
        ),
    ]
