from rest_framework import serializers

from leaseslicensing import settings
from leaseslicensing.components.invoicing.models import ChargeMethod, RepetitionType, InvoicingDetails, \
    FixedAnnualIncrementAmount, FixedAnnualIncrementPercentage, PercentageOfGrossTurnover, CrownLandRentReviewDate


class ChargeMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChargeMethod
        fields = (
            'id',
            'key',
            'display_name',
        )


class RepetitionTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepetitionType
        fields = (
            'id',
            'key',
            'display_name',
        )


class FixedAnnualIncrementAmountSerializer(serializers.ModelSerializer):
    readonly = serializers.BooleanField(read_only=True)
    to_be_deleted = serializers.SerializerMethodField()

    class Meta:
        model = FixedAnnualIncrementAmount
        fields = (
            'id',
            'year',
            'increment_amount',
            'readonly',
            'to_be_deleted',
        )
        extra_kwargs = {
            'id': {
                'read_only': False,
                'required': False,
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
            'id',
            'year',
            'increment_percentage',
            'readonly',
            'to_be_deleted',
        )
        extra_kwargs = {
            'id': {
                'read_only': False,
                'required': False,
            },
        }

    def get_to_be_deleted(self, instance):
        return False


class PercentageOfGrossTurnoverSerializer(serializers.ModelSerializer):
    readonly = serializers.BooleanField(read_only=True)
    to_be_deleted = serializers.SerializerMethodField()

    class Meta:
        model = PercentageOfGrossTurnover
        fields = (
            'id',
            'year',
            'percentage',
            'readonly',
            'to_be_deleted',
        )
        extra_kwargs = {
            'id': {
                'read_only': False,
                'required': False,
            },
        }

    def get_to_be_deleted(self, instance):
        return False


class CrownLandRentReviewDateSerializer(serializers.ModelSerializer):
    readonly = serializers.BooleanField(read_only=True)
    to_be_deleted = serializers.SerializerMethodField()

    class Meta:
        model = CrownLandRentReviewDate
        fields = (
            'id',
            'review_date',
            'readonly',
            'to_be_deleted',
        )
        extra_kwargs = {
            'id': {
                'read_only': False,
                'required': False,
            },
        }

    def get_to_be_deleted(self, instance):
        return False


class InvoicingDetailsSerializer(serializers.ModelSerializer):
    annual_increment_amounts = FixedAnnualIncrementAmountSerializer(many=True, required=False)
    annual_increment_percentages = FixedAnnualIncrementPercentageSerializer(many=True, required=False)
    gross_turnover_percentages = PercentageOfGrossTurnoverSerializer(many=True, required=False)
    crown_land_rent_review_dates = CrownLandRentReviewDateSerializer(many=True, required=False)

    class Meta:
        model = InvoicingDetails
        fields = (
            'id',
            'charge_method',                    # FK
            'base_fee_amount',
            'once_off_charge_amount',
            'review_once_every',
            'review_repetition_type',           # FK
            'invoicing_once_every',
            'invoicing_repetition_type',        # FK
            'annual_increment_amounts',         # ReverseFK
            'annual_increment_percentages',     # ReverseFK
            'gross_turnover_percentages',       # ReverseFK
            'crown_land_rent_review_dates',     # ReverseFK
        )

    def set_default_values(self, attrs, fields_excluded):
        for attr_name, value in attrs.items():
            if attr_name in ['base_fee_amount', 'once_off_charge_amount', 'review_once_every', 'review_repetition_type', 'invoicing_once_every', 'invoicing_repetition_type',]:
                if attr_name not in fields_excluded:
                    attrs[attr_name] = None  # Set default value
            elif attr_name in ['annual_increment_amounts', 'annual_increment_percentages', 'gross_turnover_percentages', 'crown_land_rent_review_dates',]:
                if attr_name not in fields_excluded:
                    for item in self.initial_data.get(attr_name):
                        item['to_be_deleted'] = True  # Mark as "to_be_deleted" to the initial value so that item is deleted at the update()

    def validate(self, attrs):
        action = self.context.get('action')

        if action == 'finance_save':
            # When "Save and Continue"/"Save and Exit" button clicked
            pass
        elif action == 'finance_complete_editing':
            # When "Complete Editing" clicked
            charge_method = attrs.get('charge_method')

            if charge_method.key == settings.CHARGE_METHOD_ONCE_OFF_CHARGE:
                self.set_default_values(attrs, [
                    'charge_method',
                    'once_off_charge_amount',
                ])
            elif charge_method.key == settings.CHARGE_METHOD_BASE_FEE_PLUS_FIXED_ANNUAL_INCREMENT:
                self.set_default_values(attrs, [
                    'charge_method',
                    'base_fee_amount',
                    'annual_increment_amounts',
                    'review_once_every',
                    'review_repetition_type',
                    'crown_land_rent_review_dates',
                    'invoicing_once_every',
                    'invoicing_repetition_type',
                ])

                annual_increment_amounts_data = attrs.get('annual_increment_amounts')
                self.validate_annual_increment(annual_increment_amounts_data)
                self.validate_crown_land_rent_review_dates(attrs)

            elif charge_method.key == settings.CHARGE_METHOD_BASE_FEE_PLUS_FIXED_ANNUAL_PERCENTAGE:
                self.set_default_values(attrs, [
                    'charge_method',
                    'base_fee_amount',
                    'annual_increment_percentages',
                    'review_once_every',
                    'review_repetition_type',
                    'crown_land_rent_review_dates',
                    'invoicing_once_every',
                    'invoicing_repetition_type',
                ])
                annual_increment_percentages_data = attrs.get('annual_increment_percentages')
                self.validate_annual_increment(annual_increment_percentages_data)
                self.validate_crown_land_rent_review_dates(attrs)
            elif charge_method.key == settings.CHARGE_METHOD_BASE_FEE_PLUS_ANNUAL_CPI:
                self.set_default_values(attrs, [
                    'charge_method',
                    'base_fee_amount',
                    'review_once_every',
                    'review_repetition_type',
                    'crown_land_rent_review_dates',
                    'invoicing_once_every',
                    'invoicing_repetition_type',
                ])
                self.validate_crown_land_rent_review_dates(attrs)
            elif charge_method.key == settings.CHARGE_METHOD_PERCENTAGE_OF_GROSS_TURNOVER:
                self.set_default_values(attrs, [
                    'charge_method',
                    'gross_turnover_percentages',
                    'invoicing_once_every',
                    'invoicing_repetition_type',
                ])
                gross_turnover_percentages_data = attrs.get('gross_turnover_percentages')
                self.validate_annual_increment(gross_turnover_percentages_data)
            elif charge_method.key == settings.CHARGE_METHOD_NO_RENT_OR_LICENCE_CHARGE:
                self.set_default_values(attrs, [])

        return attrs

    def validate_annual_increment(self, annual_increment_data):
        # Make sure there are no duplication of 'year'
        years = []
        for data in annual_increment_data:
            a_year = data.get('year')
            if a_year in years:
                raise Exception
            else:
                years.append(a_year)

    def validate_crown_land_rent_review_dates(self, attrs):
        # Make sure there are no duplication of 'date'
        crown_land_rent_review_dates_data = attrs.get('crown_land_rent_review_dates')
        dates = []
        for crown_land_rent_review_date_data in crown_land_rent_review_dates_data:
            date = crown_land_rent_review_date_data.get('review_date')
            if date in dates:
                raise Exception('Review data duplicated')
            else:
                dates.append(date)

    def update(self, instance, validated_data):
        # Local fields
        instance.base_fee_amount = validated_data.get('base_fee_amount', instance.base_fee_amount)
        instance.once_off_charge_amount = validated_data.get('once_off_charge_amount', instance.once_off_charge_amount)
        instance.review_once_every = validated_data.get('review_once_every', instance.review_once_every)
        instance.invoicing_once_every = validated_data.get('invoicing_once_every', instance.invoicing_once_every)

        # FK fields
        instance.charge_method = validated_data.get('charge_method', instance.charge_method)
        instance.review_repetition_type = validated_data.get('review_repetition_type', instance.review_repetition_type)
        instance.invoicing_repetition_type = validated_data.get('invoicing_repetition_type', instance.invoicing_repetition_type)

        # Update local and FK fields
        instance.save()

        # Reverse FKs
        annual_increment_amounts_data = validated_data.pop('annual_increment_amounts')
        annual_increment_percentages_data = validated_data.pop('annual_increment_percentages')
        gross_turnover_percentages_data = validated_data.pop('gross_turnover_percentages')
        crown_land_rent_review_dates_data = validated_data.pop('crown_land_rent_review_dates')
        self.update_annual_increment_amounts(annual_increment_amounts_data, instance)
        self.update_annual_increment_percentages(annual_increment_percentages_data, instance)
        self.update_gross_turnover_percentages(gross_turnover_percentages_data, instance)
        self.update_crown_land_rent_review_dates(crown_land_rent_review_dates_data, instance)

        return instance

    @staticmethod
    def _to_be_deleted(a_data, initial_data):
        to_be_deleted = False
        for initial_data_row in initial_data:
            if initial_data_row.get('id') == a_data.get('id'):
                if initial_data_row.get('to_be_deleted'):
                    to_be_deleted = True
                    break
        return to_be_deleted

    def update_annual_increment_amounts(self, validated_annual_increment_amounts_data, instance):
        initial_data = self.initial_data.get('annual_increment_amounts')

        for annual_increment_amount_data in validated_annual_increment_amounts_data:
            if annual_increment_amount_data.get('id', 0):
                # This data exists in the database

                # Check if it is marked as to_be_deleted
                to_be_deleted = self._to_be_deleted(annual_increment_amount_data, initial_data)

                annual_increment_amount = FixedAnnualIncrementAmount.objects.get(id=int(annual_increment_amount_data.get('id')))
                if to_be_deleted:
                    # Data is marked as to_be_deleted
                    if not annual_increment_amount.readonly:  # Double check if it's not readonly data.
                        annual_increment_amount.delete()
                else:
                    # Update data
                    serializer = FixedAnnualIncrementAmountSerializer(
                        annual_increment_amount, annual_increment_amount_data, context={'invoicing_details': instance}
                        )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
            else:
                # This is new data, not stored in the database yet.
                if 'id' in annual_increment_amount_data:
                    annual_increment_amount_data.pop('id')  # Delete the item 'id: 0' from the dictionary because we don't want to save a new record with id=0
                serializer = FixedAnnualIncrementAmountSerializer(data=annual_increment_amount_data, context={'invoicing_details': instance})
                serializer.is_valid(raise_exception=True)
                new_record = serializer.save()
                new_record.invoicing_details = instance
                new_record.save()

    def update_annual_increment_percentages(self, validated_annual_increment_percentages_data, instance):
        initial_data = self.initial_data.get('annual_increment_percentages')

        for annual_increment_percentage_data in validated_annual_increment_percentages_data:
            if annual_increment_percentage_data.get('id', 0):
                # This data exists in the database

                # Check if it is marked as to_be_deleted
                to_be_deleted = self._to_be_deleted(annual_increment_percentage_data, initial_data)

                annual_increment_percentage = FixedAnnualIncrementPercentage.objects.get(id=int(annual_increment_percentage_data.get('id')))
                if to_be_deleted:
                    # Data is marked as to_be_deleted
                    if not annual_increment_percentage.readonly:
                        annual_increment_percentage.delete()
                else:
                    # Update data
                    serializer = FixedAnnualIncrementPercentageSerializer(
                        annual_increment_percentage, annual_increment_percentage_data, context={'invoicing_details': instance}
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
            else:
                # This is new data, not stored in the database yet.
                if 'id' in annual_increment_percentage_data:
                    annual_increment_percentage_data.pop('id')  # Delete the item 'id: 0' from the dictionary because we don't want to save a new record with id=0
                serializer = FixedAnnualIncrementPercentageSerializer(data=annual_increment_percentage_data, context={'invoicing_details': instance})
                serializer.is_valid(raise_exception=True)
                new_record = serializer.save()
                new_record.invoicing_details = instance
                new_record.save()

    def update_gross_turnover_percentages(self, validated_gross_turnover_percentages_data, instance):
        initial_data = self.initial_data.get('gross_turnover_percentages')

        for gross_turnover_percentage_data in validated_gross_turnover_percentages_data:
            if gross_turnover_percentage_data.get('id', 0):
                # This data exists in the database

                # Check if it is marked as to_be_deleted
                to_be_deleted = self._to_be_deleted(gross_turnover_percentage_data, initial_data)

                gross_turnover_percentage = PercentageOfGrossTurnover.objects.get(id=int(gross_turnover_percentage_data.get('id')))
                if to_be_deleted:
                    # Data is marked as to_be_deleted
                    if not gross_turnover_percentage.readonly:
                        gross_turnover_percentage.delete()
                else:
                    # Update data
                    serializer = PercentageOfGrossTurnoverSerializer(
                        gross_turnover_percentage, gross_turnover_percentage_data, context={'invoicing_details': instance}
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
            else:
                # This is new data, not stored in the database yet.
                if 'id' in gross_turnover_percentage_data:
                    gross_turnover_percentage_data.pop('id')  # Delete the item 'id: 0' from the dictionary because we don't want to save a new record with id=0
                serializer = PercentageOfGrossTurnoverSerializer(data=gross_turnover_percentage_data, context={'invoicing_details': instance})
                serializer.is_valid(raise_exception=True)
                new_record = serializer.save()
                new_record.invoicing_details = instance
                new_record.save()

    def update_crown_land_rent_review_dates(self, validated_crown_land_rent_review_dates_data, instance):
        initial_data = self.initial_data.get('crown_land_rent_review_dates')

        for crown_land_rent_review_date_data in validated_crown_land_rent_review_dates_data:
            if crown_land_rent_review_date_data.get('id', 0):
                # This data exists in the database

                # Check if it is marked as to_be_deleted
                to_be_deleted = self._to_be_deleted(crown_land_rent_review_date_data, initial_data)

                crown_land_rent_review_date = CrownLandRentReviewDate.objects.get(id=int(crown_land_rent_review_date_data.get('id')))
                if to_be_deleted:
                    if not crown_land_rent_review_date.readonly:
                        crown_land_rent_review_date.delete()
                else:
                    serializer = CrownLandRentReviewDateSerializer(
                        crown_land_rent_review_date, crown_land_rent_review_date_data, context={'invoicing_details': instance}
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
            else:
                # This is new data, not stored in the database yet.
                if 'id' in crown_land_rent_review_date_data:
                    crown_land_rent_review_date_data.pop('id')  # Delete the item 'id: 0' from the dictionary because we don't want to save a new record with id=0
                serializer = CrownLandRentReviewDateSerializer(data=crown_land_rent_review_date_data, context={'invoicing_details': instance})
                serializer.is_valid(raise_exception=True)
                new_record = serializer.save()
                new_record.invoicing_details = instance
                new_record.save()
