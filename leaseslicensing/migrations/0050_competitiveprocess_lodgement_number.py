# Generated by Django 3.2.13 on 2022-08-04 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0049_alter_proposal_competitive_process'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitiveprocess',
            name='lodgement_number',
            field=models.CharField(blank=True, default='', max_length=9),
        ),
    ]