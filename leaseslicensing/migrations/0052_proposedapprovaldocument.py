# Generated by Django 3.2.13 on 2022-07-29 06:44

from django.db import migrations, models
import django.db.models.deletion
import leaseslicensing.components.proposals.models


class Migration(migrations.Migration):

    dependencies = [
        ('leaseslicensing', '0051_alter_approvaltype_details_placeholder'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProposedApprovalDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
                ('_file', models.FileField(max_length=512, upload_to=leaseslicensing.components.proposals.models.update_proposal_doc_filename)),
                ('input_name', models.CharField(blank=True, max_length=255, null=True)),
                ('can_delete', models.BooleanField(default=True)),
                ('can_hide', models.BooleanField(default=False)),
                ('hidden', models.BooleanField(default=False)),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proposed_approval_documents', to='leaseslicensing.proposal')),
            ],
            options={
                'verbose_name': 'Proposed Approval Document',
            },
        ),
    ]