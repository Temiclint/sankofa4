# Generated by Django 3.2.12 on 2022-06-17 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0027_rename_percentage_discount_rate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoicesetting',
            name='email_notification',
        ),
    ]
