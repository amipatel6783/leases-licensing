import logging
import os
from datetime import date

from django.core.files import File
from django.utils import timezone
from ledger_api_client.managed_models import SystemGroup

from leaseslicensing import settings
from leaseslicensing.components.invoicing.models import (
    ChargeMethod,
    CPICalculationMethod,
    InvoicingAndReviewDates,
    RepetitionType,
)
from leaseslicensing.components.main.models import ApplicationType, GlobalSettings
from leaseslicensing.components.proposals.models import ProposalType

logger = logging.getLogger(__name__)


class DefaultDataManager:
    def __init__(self):
        # Proposal Types
        for item in settings.PROPOSAL_TYPES:
            try:
                myType, created = ProposalType.objects.get_or_create(code=item[0])
                if created:
                    myType.description = item[1]
                    myType.save()
                    logger.info(f"Created ProposalType: {item[1]}")
            except Exception as e:
                logger.error(f"{e}, ProposalType: {item[1]}")

        # Application Types
        for item in settings.APPLICATION_TYPES:
            try:
                myType, created = ApplicationType.objects.get_or_create(name=item[0])
                if created:
                    # myType.description = item[1]
                    # myType.save()
                    logger.info(f"Created ApplicationType: {item[1]}")
            except Exception as e:
                logger.error(f"{e}, ApplicationType: {item[1]}")

        # Store
        for item in GlobalSettings.keys:
            try:
                obj, created = GlobalSettings.objects.get_or_create(key=item[0])
                if created:
                    if item[0] in GlobalSettings.keys_for_file:
                        with open(
                            GlobalSettings.default_values[item[0]], "rb"
                        ) as doc_file:
                            obj._file.save(
                                os.path.basename(
                                    GlobalSettings.default_values[item[0]]
                                ),
                                File(doc_file),
                                save=True,
                            )
                        obj.save()
                    else:
                        obj.value = item[1]
                        obj.save()
                    logger.info(f"Created {item[0]}: {item[1]}")
            except Exception as e:
                logger.error(f"{e}, Key: {item[0]}")

        for item in settings.CHARGE_METHODS:
            try:
                myMethod, created = ChargeMethod.objects.get_or_create(key=item[0])
                if created:
                    myMethod.display_name = item[1]
                    myMethod.save()
                    logger.info(f"Created ChargeMethod: {item[1]}")
            except Exception as e:
                logger.error(f"{e}, ChargeMethod: {item[1]}")

        for item in settings.REPETITION_TYPES:
            try:
                myType, created = RepetitionType.objects.get_or_create(key=item[0])
                if created:
                    myType.display_name = item[1]
                    myType.save()
                    logger.info(f"Created RepetitionType: {item[1]}")
            except Exception as e:
                logger.error(f"{e}, RepetitionType: {item[1]}")

        for item in settings.CPI_CALCULATION_METHODS:
            try:
                myType, created = CPICalculationMethod.objects.get_or_create(
                    name=item[0]
                )
                if created:
                    myType.display_name = item[1]
                    myType.save()
                    logger.info(f"Created CPICalculationMethod: {item[1]}")
            except Exception as e:
                logger.error(f"{e}, CPICalculationMethod: {item[1]}")

        for a_group in settings.GROUP_NAME_CHOICES:
            try:
                myGroup, created = SystemGroup.objects.get_or_create(
                    name=a_group[0]
                )  # Should name be a_group[1]???
                if created:
                    logger.info(f"Created SystemGroup: {item[0]}")
            except Exception as e:
                logger.error(f"{e}, SystemGroup: {item[1]}")

        year = timezone.now().year
        for year in range(year, year + 100):
            try:
                InvoicingAndReviewDates.objects.get(
                    year=year,
                )
            except InvoicingAndReviewDates.DoesNotExist:
                InvoicingAndReviewDates.objects.create(
                    year=year,
                    invoicing_date_annually=date(year, 1, 1),
                    review_date_annually=date(year, 1, 1),
                )
