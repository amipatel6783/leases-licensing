# Generated by Django 3.2.18 on 2023-07-19 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0218_cpicalculationmethod_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvaltype',
            name='invoices_exclude_gst',
            field=models.BooleanField(default=False),
        ),
    ]
