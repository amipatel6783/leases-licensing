# Generated by Django 3.2.18 on 2023-08-21 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0245_auto_20230816_1600'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation',
            name='application_discount',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='apply_application_discount',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='apply_licence_discount',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='bpay_allowed',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='charge_once_per_year',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='event_training_completed',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='event_training_date',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='last_event_application_fee_date',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='licence_discount',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='max_num_months_ahead',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='monthly_invoicing_allowed',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='monthly_invoicing_period',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='monthly_payment_due_period',
        ),
        migrations.RemoveField(
            model_name='usersystemsettings',
            name='event_training_completed',
        ),
        migrations.RemoveField(
            model_name='usersystemsettings',
            name='event_training_date',
        ),
        migrations.DeleteModel(
            name='ApplicationFeeDiscount',
        ),
    ]
