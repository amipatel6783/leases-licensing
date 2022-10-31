# Generated by Django 3.2.4 on 2022-02-07 02:12

from django.db import migrations, models
import django.db.models.deletion
import leaseslicensing.components.proposals.models


class Migration(migrations.Migration):

    dependencies = [
        ("leaseslicensing", "0029_alter_proposal_submitter"),
    ]

    operations = [
        migrations.CreateModel(
            name="StaffingDocument",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=255, verbose_name="name"),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                ("uploaded_date", models.DateTimeField(auto_now_add=True)),
                (
                    "_file",
                    models.FileField(
                        max_length=512,
                        upload_to=leaseslicensing.components.proposals.models.update_proposal_doc_filename,
                    ),
                ),
                ("input_name", models.CharField(blank=True, max_length=255, null=True)),
                ("can_delete", models.BooleanField(default=True)),
                ("can_hide", models.BooleanField(default=False)),
                ("hidden", models.BooleanField(default=False)),
                (
                    "proposal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="staffing_documents",
                        to="leaseslicensing.proposal",
                    ),
                ),
            ],
            options={
                "verbose_name": "Application Document",
            },
        ),
        migrations.CreateModel(
            name="RiskFactorsDocument",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=255, verbose_name="name"),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                ("uploaded_date", models.DateTimeField(auto_now_add=True)),
                (
                    "_file",
                    models.FileField(
                        max_length=512,
                        upload_to=leaseslicensing.components.proposals.models.update_proposal_doc_filename,
                    ),
                ),
                ("input_name", models.CharField(blank=True, max_length=255, null=True)),
                ("can_delete", models.BooleanField(default=True)),
                ("can_hide", models.BooleanField(default=False)),
                ("hidden", models.BooleanField(default=False)),
                (
                    "proposal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="risk_factors_documents",
                        to="leaseslicensing.proposal",
                    ),
                ),
            ],
            options={
                "verbose_name": "Application Document",
            },
        ),
        migrations.CreateModel(
            name="ProfitAndLossDocument",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=255, verbose_name="name"),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                ("uploaded_date", models.DateTimeField(auto_now_add=True)),
                (
                    "_file",
                    models.FileField(
                        max_length=512,
                        upload_to=leaseslicensing.components.proposals.models.update_proposal_doc_filename,
                    ),
                ),
                ("input_name", models.CharField(blank=True, max_length=255, null=True)),
                ("can_delete", models.BooleanField(default=True)),
                ("can_hide", models.BooleanField(default=False)),
                ("hidden", models.BooleanField(default=False)),
                (
                    "proposal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profit_and_loss_documents",
                        to="leaseslicensing.proposal",
                    ),
                ),
            ],
            options={
                "verbose_name": "Application Document",
            },
        ),
        migrations.CreateModel(
            name="MarketAnalysisDocument",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=255, verbose_name="name"),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                ("uploaded_date", models.DateTimeField(auto_now_add=True)),
                (
                    "_file",
                    models.FileField(
                        max_length=512,
                        upload_to=leaseslicensing.components.proposals.models.update_proposal_doc_filename,
                    ),
                ),
                ("input_name", models.CharField(blank=True, max_length=255, null=True)),
                ("can_delete", models.BooleanField(default=True)),
                ("can_hide", models.BooleanField(default=False)),
                ("hidden", models.BooleanField(default=False)),
                (
                    "proposal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="market_analysis_documents",
                        to="leaseslicensing.proposal",
                    ),
                ),
            ],
            options={
                "verbose_name": "Application Document",
            },
        ),
        migrations.CreateModel(
            name="LegislativeRequirementsDocument",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=255, verbose_name="name"),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                ("uploaded_date", models.DateTimeField(auto_now_add=True)),
                (
                    "_file",
                    models.FileField(
                        max_length=512,
                        upload_to=leaseslicensing.components.proposals.models.update_proposal_doc_filename,
                    ),
                ),
                ("input_name", models.CharField(blank=True, max_length=255, null=True)),
                ("can_delete", models.BooleanField(default=True)),
                ("can_hide", models.BooleanField(default=False)),
                ("hidden", models.BooleanField(default=False)),
                (
                    "proposal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="legislative_requirements_documents",
                        to="leaseslicensing.proposal",
                    ),
                ),
            ],
            options={
                "verbose_name": "Application Document",
            },
        ),
        migrations.CreateModel(
            name="KeyPersonnelDocument",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=255, verbose_name="name"),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                ("uploaded_date", models.DateTimeField(auto_now_add=True)),
                (
                    "_file",
                    models.FileField(
                        max_length=512,
                        upload_to=leaseslicensing.components.proposals.models.update_proposal_doc_filename,
                    ),
                ),
                ("input_name", models.CharField(blank=True, max_length=255, null=True)),
                ("can_delete", models.BooleanField(default=True)),
                ("can_hide", models.BooleanField(default=False)),
                ("hidden", models.BooleanField(default=False)),
                (
                    "proposal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="key_personnel_documents",
                        to="leaseslicensing.proposal",
                    ),
                ),
            ],
            options={
                "verbose_name": "Application Document",
            },
        ),
        migrations.CreateModel(
            name="KeyMilestonesDocument",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=255, verbose_name="name"),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                ("uploaded_date", models.DateTimeField(auto_now_add=True)),
                (
                    "_file",
                    models.FileField(
                        max_length=512,
                        upload_to=leaseslicensing.components.proposals.models.update_proposal_doc_filename,
                    ),
                ),
                ("input_name", models.CharField(blank=True, max_length=255, null=True)),
                ("can_delete", models.BooleanField(default=True)),
                ("can_hide", models.BooleanField(default=False)),
                ("hidden", models.BooleanField(default=False)),
                (
                    "proposal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="key_milestones_documents",
                        to="leaseslicensing.proposal",
                    ),
                ),
            ],
            options={
                "verbose_name": "Application Document",
            },
        ),
        migrations.CreateModel(
            name="FinancialCapacityDocument",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=255, verbose_name="name"),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                ("uploaded_date", models.DateTimeField(auto_now_add=True)),
                (
                    "_file",
                    models.FileField(
                        max_length=512,
                        upload_to=leaseslicensing.components.proposals.models.update_proposal_doc_filename,
                    ),
                ),
                ("input_name", models.CharField(blank=True, max_length=255, null=True)),
                ("can_delete", models.BooleanField(default=True)),
                ("can_hide", models.BooleanField(default=False)),
                ("hidden", models.BooleanField(default=False)),
                (
                    "proposal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="financial_capacity_documents",
                        to="leaseslicensing.proposal",
                    ),
                ),
            ],
            options={
                "verbose_name": "Application Document",
            },
        ),
        migrations.CreateModel(
            name="CashFlowDocument",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=255, verbose_name="name"),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                ("uploaded_date", models.DateTimeField(auto_now_add=True)),
                (
                    "_file",
                    models.FileField(
                        max_length=512,
                        upload_to=leaseslicensing.components.proposals.models.update_proposal_doc_filename,
                    ),
                ),
                ("input_name", models.CharField(blank=True, max_length=255, null=True)),
                ("can_delete", models.BooleanField(default=True)),
                ("can_hide", models.BooleanField(default=False)),
                ("hidden", models.BooleanField(default=False)),
                (
                    "proposal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cash_flow_documents",
                        to="leaseslicensing.proposal",
                    ),
                ),
            ],
            options={
                "verbose_name": "Application Document",
            },
        ),
        migrations.CreateModel(
            name="CapitalInvestmentDocument",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=255, verbose_name="name"),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                ("uploaded_date", models.DateTimeField(auto_now_add=True)),
                (
                    "_file",
                    models.FileField(
                        max_length=512,
                        upload_to=leaseslicensing.components.proposals.models.update_proposal_doc_filename,
                    ),
                ),
                ("input_name", models.CharField(blank=True, max_length=255, null=True)),
                ("can_delete", models.BooleanField(default=True)),
                ("can_hide", models.BooleanField(default=False)),
                ("hidden", models.BooleanField(default=False)),
                (
                    "proposal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="capital_investment_documents",
                        to="leaseslicensing.proposal",
                    ),
                ),
            ],
            options={
                "verbose_name": "Application Document",
            },
        ),
        migrations.CreateModel(
            name="AvailableActivitiesDocument",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(blank=True, max_length=255, verbose_name="name"),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                ("uploaded_date", models.DateTimeField(auto_now_add=True)),
                (
                    "_file",
                    models.FileField(
                        max_length=512,
                        upload_to=leaseslicensing.components.proposals.models.update_proposal_doc_filename,
                    ),
                ),
                ("input_name", models.CharField(blank=True, max_length=255, null=True)),
                ("can_delete", models.BooleanField(default=True)),
                ("can_hide", models.BooleanField(default=False)),
                ("hidden", models.BooleanField(default=False)),
                (
                    "proposal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="available_activities_documents",
                        to="leaseslicensing.proposal",
                    ),
                ),
            ],
            options={
                "verbose_name": "Application Document",
            },
        ),
    ]