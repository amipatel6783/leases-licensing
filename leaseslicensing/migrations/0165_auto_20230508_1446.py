# Generated by Django 3.2.18 on 2023-05-08 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0164_proposalact_proposalcategory_proposaltenure'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProposalDistrict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='leaseslicensing.district')),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='districts', to='leaseslicensing.proposal')),
            ],
            options={
                'unique_together': {('proposal', 'district')},
            },
        ),
        migrations.CreateModel(
            name='ProposalLGA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lga', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='leaseslicensing.lga')),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='lgas', to='leaseslicensing.proposal')),
            ],
            options={
                'unique_together': {('proposal', 'lga')},
            },
        ),
        migrations.CreateModel(
            name='ProposalRegion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='regions', to='leaseslicensing.proposal')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='leaseslicensing.region')),
            ],
            options={
                'unique_together': {('proposal', 'region')},
            },
        ),
        migrations.DeleteModel(
            name='ProposalLocality',
        ),
    ]