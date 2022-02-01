from django.contrib import admin
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from leaseslicensing.components.proposals import models
from leaseslicensing.components.bookings.models import ApplicationFeeInvoice
from leaseslicensing.components.proposals import forms
from leaseslicensing.components.main.models import (
    SystemMaintenance,
    ApplicationType,
    OracleCode,
    RequiredDocument,
    Question,
    GlobalSettings,
)
from django.conf.urls import url
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect
from leaseslicensing.utils import create_helppage_object
# Register your models here.

# Commented since COLS does not use schema - so will not require direct editing by user in Admin (although a ProposalType is still required for ApplicationType)
#@admin.register(models.ProposalType)
class ProposalTypeAdmin(admin.ModelAdmin):
    list_display = ['name','description', 'version']
    ordering = ('name', '-version')
    list_filter = ('name',)
    #exclude=("site",)

class ProposalDocumentInline(admin.TabularInline):
    model = models.ProposalDocument
    extra = 0

@admin.register(models.AmendmentReason)
class AmendmentReasonAdmin(admin.ModelAdmin):
    list_display = ['reason']

@admin.register(models.Proposal)
#class ProposalAdmin(VersionAdmin):
class ProposalAdmin(admin.ModelAdmin):
    inlines =[ProposalDocumentInline,]

@admin.register(models.ProposalStandardRequirement)
class ProposalStandardRequirementAdmin(admin.ModelAdmin):
    list_display = ['code','text','obsolete', 'application_type', 'participant_number_required', 'default']

#@admin.register(models.HelpPage)
class HelpPageAdmin(admin.ModelAdmin):
    list_display = ['application_type','help_type', 'description', 'version']
    form = forms.LeasesLicensingHelpPageAdminForm
    change_list_template = "leaseslicensing/help_page_changelist.html"
    ordering = ('application_type', 'help_type', '-version')
    list_filter = ('application_type', 'help_type')


    def get_urls(self):
        urls = super(HelpPageAdmin, self).get_urls()
        my_urls = [
            url('create_leaseslicensing_help/', self.admin_site.admin_view(self.create_leaseslicensing_help)),
            url('create_leaseslicensing_help_assessor/', self.admin_site.admin_view(self.create_leaseslicensing_help_assessor)),
        ]
        return my_urls + urls

    def create_leaseslicensing_help(self, request):
        create_helppage_object(application_type='T Class', help_type=models.HelpPage.HELP_TEXT_EXTERNAL)
        return HttpResponseRedirect("../")

    def create_leaseslicensing_help_assessor(self, request):
        create_helppage_object(application_type='T Class', help_type=models.HelpPage.HELP_TEXT_INTERNAL)
        return HttpResponseRedirect("../")

@admin.register(models.ChecklistQuestion)
class ChecklistQuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'application_type','list_type', 'obsolete','answer_type', 'order']
    ordering = ('order',)

@admin.register(SystemMaintenance)
class SystemMaintenanceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'start_date', 'end_date', 'duration']
    ordering = ('start_date',)
    readonly_fields = ('duration',)
    form = forms.SystemMaintenanceAdminForm

@admin.register(ApplicationType)
class ApplicationTypeAdmin(admin.ModelAdmin):
    #list_display = ['name', 'order', 'visible', 'max_renewals', 'max_renewal_period', 'application_fee']
    ordering = ('order',)
    readonly_fields = ['name']


class OracleCodeInline(admin.TabularInline):
    model = OracleCode
    exclude = ['archive_date']
    extra = 3
    max_num = 3
    can_delete = False

@admin.register(RequiredDocument)
class RequiredDocumentAdmin(admin.ModelAdmin):
    pass

@admin.register(GlobalSettings)
class GlobalSettingsAdmin(admin.ModelAdmin):
    list_display = ['key', 'value']
    ordering = ('key',)

@admin.register(models.ReferralRecipientGroup)
class ReferralRecipientGroupAdmin(admin.ModelAdmin):
    #filter_horizontal = ('members',)
    list_display = ['name']
    exclude = ('site',)
    actions = None

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "members":
            kwargs["queryset"] = EmailUser.objects.filter(is_staff=True)
        return super(ReferralRecipientGroupAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

@admin.register(models.QAOfficerGroup)
class QAOfficerGroupAdmin(admin.ModelAdmin):
    #filter_horizontal = ('members',)
    list_display = ['name']
    exclude = ('site',)
    actions = None

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "members":
            #kwargs["queryset"] = EmailUser.objects.filter(email__icontains='@dbca.wa.gov.au')
            kwargs["queryset"] = EmailUser.objects.filter(is_staff=True)
        return super(QAOfficerGroupAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    #list_display = ['id','name', 'visible']
    list_display = ['name']
    ordering = ('id',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'answer_one', 'answer_two', 'answer_three', 'answer_four', 'application_type',]
    ordering = ('question_text',)


