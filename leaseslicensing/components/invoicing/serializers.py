import logging

from dateutil.relativedelta import relativedelta
from rest_framework import serializers

from leaseslicensing import settings
from leaseslicensing.components.approvals.models import ApprovalUserAction
from leaseslicensing.components.invoicing.models import (
    ChargeMethod,
    CPICalculationMethod,
    CrownLandRentReviewDate,
    CustomCPIYear,
    FinancialMonth,
    FinancialQuarter,
    FixedAnnualIncrementAmount,
    FixedAnnualIncrementPercentage,
    Invoice,
    InvoiceTransaction,
    InvoicingDetails,
    PercentageOfGrossTurnover,
    RepetitionType,
)
from leaseslicensing.helpers import is_customer, is_finance_officer, today

logger = logging.getLogger(__name__)


class ChargeMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeMethod
        fields = (
            "id",
            "key",
            "display_name",
        )


class RepetitionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepetitionType
        fields = (
            "id",
            "key",
            "display_name",
        )


class CPICalculationMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPICalculationMethod
        fields = (
            "id",
            "name",
            "display_name",
        )


class FixedAnnualIncrementAmountSerializer(serializers.ModelSerializer):
    readonly = serializers.BooleanField(read_only=True)
    to_be_deleted = serializers.SerializerMethodField()

    class Meta:
        model = FixedAnnualIncrementAmount
        fields = (
            "id",
            "year",
            "increment_amount",
            "readonly",
            "to_be_deleted",
        )
        extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
        }

    def get_to_be_deleted(self, instance):
        return False


class FixedAnnualIncrementPercentageSerializer(serializers.ModelSerializer):
    readonly = serializers.BooleanField(read_only=True)
    to_be_deleted = serializers.SerializerMethodField()

    class Meta:
        model = FixedAnnualIncrementPercentage
        fields = (
            "id",
            "year",
            "increment_percentage",
            "readonly",
            "to_be_deleted",
        )
        extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
        }

    def get_to_be_deleted(self, instance):
        return False


class FinancialMonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialMonth
        fields = ["year", "month", "gross_turnover", "locked"]


class FinancialQuarterSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialQuarter
        fields = ["quarter", "gross_turnover", "locked"]


class PercentageOfGrossTurnoverSerializer(serializers.ModelSerializer):
    to_be_deleted = serializers.SerializerMethodField()
    quarters = FinancialQuarterSerializer(many=True, required=False)
    months = FinancialMonthSerializer(many=True, required=False)

    class Meta:
        model = PercentageOfGrossTurnover
        fields = (
            "id",
            "year",
            "financial_year",
            "percentage",
            "gross_turnover",
            "locked",
            "to_be_deleted",
            "quarters",
            "months",
        )
        extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
        }

    def get_to_be_deleted(self, instance):
        return False

    def create(self, validated_data):
        quarters = validated_data.pop("quarters", [])
        months = validated_data.pop("months", [])
        instance = super().create(validated_data)
        self.get_or_create_quarters(quarters, instance)
        self.get_or_create_months(months, instance)
        return instance

    def update(self, instance, validated_data):
        quarters = validated_data.pop("quarters", [])
        months = validated_data.pop("months", [])
        self.get_or_create_quarters(quarters, instance)
        self.get_or_create_months(months, instance)
        return super().update(instance, validated_data)

    def get_or_create_quarters(self, quarters, instance):
        if quarters:
            for quarter_data in quarters:
                quarter, created = FinancialQuarter.objects.get_or_create(
                    year=instance,
                    quarter=quarter_data.get("quarter"),
                )
                gross_turnover = quarter_data.get("gross_turnover")
                if gross_turnover:
                    quarter.gross_turnover = gross_turnover
                    quarter.save()

    def get_or_create_months(self, months, instance):
        if months:
            for month_data in months:
                month, created = FinancialMonth.objects.get_or_create(
                    financial_year=instance,
                    year=month_data.get("year"),
                    month=month_data.get("month"),
                )
                gross_turnover = month_data.get("gross_turnover")
                if gross_turnover:
                    month.gross_turnover = gross_turnover
                    month.save()


class CrownLandRentReviewDateSerializer(serializers.ModelSerializer):
    readonly = serializers.BooleanField(read_only=True)
    to_be_deleted = serializers.SerializerMethodField()

    class Meta:
        model = CrownLandRentReviewDate
        fields = (
            "id",
            "review_date",
            "readonly",
            "to_be_deleted",
        )
        extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
        }

    def get_to_be_deleted(self, instance):
        return False


class CustomCPIYearSerializer(serializers.ModelSerializer):
    has_passed = serializers.SerializerMethodField()

    class Meta:
        model = CustomCPIYear
        fields = (
            "id",
            "year",
            "label",
            "percentage",
            "has_passed",
        )

    def get_has_passed(self, instance):
        start_date = instance.invoicing_details.approval.start_date
        if instance.year > 1:
            start_date = start_date + relativedelta(years=instance.year - 1)
        return not start_date > today()


class InvoicingDetailsSerializer(serializers.ModelSerializer):
    charge_method_key = serializers.CharField(
        source="charge_method.key", read_only=True
    )
    annual_increment_amounts = FixedAnnualIncrementAmountSerializer(
        many=True, required=False
    )
    annual_increment_percentages = FixedAnnualIncrementPercentageSerializer(
        many=True, required=False
    )
    gross_turnover_percentages = PercentageOfGrossTurnoverSerializer(
        many=True, required=False
    )
    custom_cpi_years = CustomCPIYearSerializer(many=True, required=False)
    comment_text = serializers.CharField(required=False)

    class Meta:
        model = InvoicingDetails
        fields = (
            "id",
            "charge_method",  # FK
            "charge_method_key",
            "base_fee_amount",
            "once_off_charge_amount",
            "review_once_every",
            "review_repetition_type",  # FK
            "invoicing_once_every",
            "invoicing_repetition_type",  # FK
            "invoicing_month_of_year",
            "invoicing_day_of_month",
            "annual_increment_amounts",  # ReverseFK
            "annual_increment_percentages",  # ReverseFK
            "gross_turnover_percentages",  # ReverseFK
            "custom_cpi_years",  # ReverseFK
            "cpi_calculation_method",
            "comment_text",
        )

    def set_default_values(self, attrs, fields_excluded):
        for attr_name, value in attrs.items():
            if attr_name in [
                "base_fee_amount",
                "once_off_charge_amount",
                "review_once_every",
                "review_repetition_type",
                "invoicing_once_every",
                "invoicing_repetition_type",
                # "cpi_calculation_method",
            ]:
                if attr_name not in fields_excluded:
                    attrs[attr_name] = None  # Set default value
            elif attr_name in [
                "annual_increment_amounts",
                "annual_increment_percentages",
                "gross_turnover_percentages",
            ]:
                if attr_name not in fields_excluded:
                    for item in self.initial_data.get(attr_name):
                        item[
                            "to_be_deleted"
                        ] = True  # Mark as "to_be_deleted" to the initial value so that item is deleted at the update()

    def validate(self, attrs):
        field_errors = {}
        non_field_errors = []

        action = self.context.get("action")

        if action in ["finance_save", "finance_complete_editing"]:
            # When "Complete Editing" clicked
            charge_method = attrs.get("charge_method")

            if not charge_method:
                raise serializers.ValidationError(["No charge method selected"])

            if charge_method.key == settings.CHARGE_METHOD_ONCE_OFF_CHARGE:
                self.set_default_values(
                    attrs,
                    [
                        "charge_method",
                        "once_off_charge_amount",
                    ],
                )
            elif (
                charge_method.key
                == settings.CHARGE_METHOD_BASE_FEE_PLUS_FIXED_ANNUAL_INCREMENT
            ):
                self.set_default_values(
                    attrs,
                    [
                        "charge_method",
                        "base_fee_amount",
                        "annual_increment_amounts",
                        "review_once_every",
                        "review_repetition_type",
                        "invoicing_once_every",
                        "invoicing_repetition_type",
                    ],
                )

                annual_increment_amounts_data = attrs.get("annual_increment_amounts")
                self._validate_annual_increment(
                    annual_increment_amounts_data, field_errors, non_field_errors
                )

            elif (
                charge_method.key
                == settings.CHARGE_METHOD_BASE_FEE_PLUS_FIXED_ANNUAL_PERCENTAGE
            ):
                self.set_default_values(
                    attrs,
                    [
                        "charge_method",
                        "base_fee_amount",
                        "annual_increment_percentages",
                        "review_once_every",
                        "review_repetition_type",
                        "invoicing_once_every",
                        "invoicing_repetition_type",
                    ],
                )
                annual_increment_percentages_data = attrs.get(
                    "annual_increment_percentages"
                )
                self._validate_annual_increment(
                    annual_increment_percentages_data, field_errors, non_field_errors
                )
            elif charge_method.key == settings.CHARGE_METHOD_BASE_FEE_PLUS_ANNUAL_CPI:
                self.set_default_values(
                    attrs,
                    [
                        "charge_method",
                        "base_fee_amount",
                        "review_once_every",
                        "review_repetition_type",
                        "invoicing_once_every",
                        "invoicing_repetition_type",
                        "cpi_calculation_method",
                    ],
                )
            elif (
                charge_method.key == settings.CHARGE_METHOD_PERCENTAGE_OF_GROSS_TURNOVER
            ):
                self.set_default_values(
                    attrs,
                    [
                        "charge_method",
                        "gross_turnover_percentages",
                        "invoicing_once_every",
                        "invoicing_repetition_type",
                    ],
                )
                gross_turnover_percentages_data = attrs.get(
                    "gross_turnover_percentages"
                )
                self._validate_annual_increment(
                    gross_turnover_percentages_data, field_errors, non_field_errors
                )
            elif charge_method.key == settings.CHARGE_METHOD_NO_RENT_OR_LICENCE_CHARGE:
                self.set_default_values(attrs, [])

        # Raise errors
        if field_errors:
            raise serializers.ValidationError(field_errors)
        # Raise errors
        if non_field_errors:
            raise serializers.ValidationError(non_field_errors)

        return attrs

    def _validate_annual_increment(
        self, annual_increment_data, field_errors, non_field_errors
    ):
        # Make sure there are no duplication of 'year'
        years = []
        for data in annual_increment_data:
            a_year = data.get("year")
            if a_year in years:
                non_field_errors.append(
                    f"Year: {str(a_year)} is duplicated. It must be unique."
                )
            else:
                years.append(a_year)

    def update(self, instance, validated_data):
        # Not really sure the following code is needed up to instance.save()
        # As could just call super().update(instance, validated_data) to achieve the same result?
        # Local fields

        if "comment_text" in validated_data:
            # When editing from the approval details page log the reason the edit was made
            comment_text = validated_data.pop("comment_text")
            instance.approval.log_user_action(
                ApprovalUserAction.ACTION_UPDATE_APPROVAL_INVOICING_DETAILS.format(
                    instance.approval.lodgement_number, comment_text
                ),
                self.context["request"],
            )

        if instance.base_fee_amount != validated_data.get("base_fee_amount"):
            instance.approval.log_user_action(
                ApprovalUserAction.ACTION_REVIEW_INVOICING_DETAILS_BASE_FEE_APPROVAL.format(
                    instance.base_fee_amount, validated_data.get("base_fee_amount")
                ),
                self.context["request"],
            )
        instance.base_fee_amount = validated_data.get(
            "base_fee_amount", instance.base_fee_amount
        )

        instance.once_off_charge_amount = validated_data.get(
            "once_off_charge_amount", instance.once_off_charge_amount
        )
        instance.review_once_every = validated_data.get(
            "review_once_every", instance.review_once_every
        )
        instance.invoicing_once_every = validated_data.get(
            "invoicing_once_every", instance.invoicing_once_every
        )
        instance.invoicing_day_of_month = validated_data.get(
            "invoicing_day_of_month", instance.invoicing_day_of_month
        )
        instance.invoicing_month_of_year = validated_data.get(
            "invoicing_month_of_year", instance.invoicing_month_of_year
        )

        # FK fields
        instance.charge_method = validated_data.get(
            "charge_method", instance.charge_method
        )
        instance.review_repetition_type = validated_data.get(
            "review_repetition_type", instance.review_repetition_type
        )
        instance.invoicing_repetition_type = validated_data.get(
            "invoicing_repetition_type", instance.invoicing_repetition_type
        )
        instance.cpi_calculation_method = validated_data.get(
            "cpi_calculation_method", instance.cpi_calculation_method
        )

        # Update local and FK fields
        instance.save()

        # Reverse FKs
        annual_increment_amounts_data = validated_data.pop("annual_increment_amounts")
        annual_increment_percentages_data = validated_data.pop(
            "annual_increment_percentages"
        )
        gross_turnover_percentages_data = validated_data.pop(
            "gross_turnover_percentages"
        )
        custom_cpi_years_data = validated_data.pop("custom_cpi_years")
        self.update_annual_increment_amounts(annual_increment_amounts_data, instance)
        self.update_annual_increment_percentages(
            annual_increment_percentages_data, instance
        )
        self.update_gross_turnover_percentages(
            gross_turnover_percentages_data, instance
        )
        self.update_custom_cpi_years(custom_cpi_years_data, instance)
        return instance

    @staticmethod
    def _to_be_deleted(a_data, initial_data):
        to_be_deleted = False
        for initial_data_row in initial_data:
            if initial_data_row.get("id") == a_data.get("id"):
                if initial_data_row.get("to_be_deleted"):
                    to_be_deleted = True
                    break
        return to_be_deleted

    def update_annual_increment_amounts(
        self, validated_annual_increment_amounts_data, instance
    ):
        # Todo: Deal with the case where the approval duration is shortened
        # and one or more annual increment amounts need to be deleted
        for annual_increment_amount_data in validated_annual_increment_amounts_data:
            (
                annual_increment_amount,
                created,
            ) = FixedAnnualIncrementAmount.objects.get_or_create(
                invoicing_details=instance,
                year=annual_increment_amount_data.get("year"),
            )

            logger.debug(f"annual_increment_amount: {annual_increment_amount}")
            logger.debug(f"created: {created}")

            serializer = FixedAnnualIncrementAmountSerializer(
                annual_increment_amount,
                data=annual_increment_amount_data,
                context={"invoicing_details": instance},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

    def update_annual_increment_percentages(
        self, validated_annual_increment_percentages_data, instance
    ):
        # Todo: Deal with the case where the approval duration is shortened
        # and one or more annual increment amounts need to be deleted
        for (
            annual_increment_percentage_data
        ) in validated_annual_increment_percentages_data:
            (
                annual_increment_percentage,
                created,
            ) = FixedAnnualIncrementPercentage.objects.get_or_create(
                invoicing_details=instance,
                year=annual_increment_percentage_data.get("year"),
            )

            serializer = FixedAnnualIncrementPercentageSerializer(
                annual_increment_percentage,
                data=annual_increment_percentage_data,
                context={"invoicing_details": instance},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

    def update_gross_turnover_percentages(
        self, validated_gross_turnover_percentages_data, instance
    ):
        for gross_turnover_percentage_data in validated_gross_turnover_percentages_data:
            (
                gross_turnover_percentage,
                created,
            ) = PercentageOfGrossTurnover.objects.get_or_create(
                invoicing_details=instance,
                year=gross_turnover_percentage_data.get("year"),
            )

            serializer = PercentageOfGrossTurnoverSerializer(
                gross_turnover_percentage,
                data=gross_turnover_percentage_data,
                context={"invoicing_details": instance},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

    def update_custom_cpi_years(self, validated_custom_cpi_years, instance):
        for custom_cpi_year_data in validated_custom_cpi_years:
            custom_cpi_year, created = CustomCPIYear.objects.get_or_create(
                invoicing_details=instance, year=custom_cpi_year_data.get("year")
            )
            custom_cpi_year.label = custom_cpi_year_data["label"]
            if "percentage" in custom_cpi_year_data:
                custom_cpi_year.percentage = custom_cpi_year_data["percentage"]
            custom_cpi_year.save()


class InvoiceSerializer(serializers.ModelSerializer):
    approval_lodgement_number = serializers.CharField(
        source="approval.lodgement_number", read_only=True
    )
    # update this once we have a proper approval_type field on the approval object
    approval_type = serializers.SerializerMethodField()
    holder = serializers.CharField(source="approval.holder", read_only=True)
    invoice_pdf_secure_url = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    is_finance_officer = serializers.SerializerMethodField()
    is_customer = serializers.SerializerMethodField()
    transaction_count = serializers.IntegerField(
        source="transactions.count", read_only=True
    )
    balance = serializers.DecimalField(max_digits=9, decimal_places=2, read_only=True)

    class Meta:
        model = Invoice
        fields = [
            "id",
            "lodgement_number",
            "approval",
            "approval_lodgement_number",
            "approval_type",
            "holder",
            "status",
            "status_display",
            "invoice_pdf_secure_url",
            "ledger_invoice_url",
            "oracle_invoice_number",
            "amount",
            "transaction_count",
            "balance",
            "gst_free",
            "date_issued",
            "date_due",
            "is_finance_officer",
            "is_customer",
        ]
        datatables_always_serialize = [
            "status",
            "transaction_count",
            "balance",
            "is_finance_officer",
            "oracle_invoice_number",
            "is_customer",
        ]

    def get_approval_type(self, obj):
        # update this once we have a proper approval_type field on the approval object
        return obj.approval.approval_type.name

    def get_invoice_pdf_secure_url(self, obj):
        if obj.invoice_pdf:
            return (
                f"/api/main/secure_file/{self.Meta.model._meta.model.__name__}/{obj.id}/invoice_pdf/",
            )

        return None

    def get_is_finance_officer(self, obj):
        request = self.context.get("request")
        return is_finance_officer(request)

    def get_is_customer(self, obj):
        request = self.context.get("request")
        return is_customer(request)


class InvoiceEditOracleInvoiceNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            "id",
            "invoice_pdf",
            "oracle_invoice_number",
            "date_issued",
            "date_due",
            "oracle_invoice_number",
            "status",
        ]


class InvoiceTransactionSerializer(serializers.ModelSerializer):
    cumulative_balance = serializers.DecimalField(
        read_only=True, max_digits=9, decimal_places=2
    )

    class Meta:
        model = InvoiceTransaction
        fields = "__all__"
