from django.contrib import admin

from .educational_content.models import EducationalContent, PaymentScheduleItem
from .nafath_center.models import PaymentScheduleRow, NafathCenterAgreement


# ---------------- EducationalContent ----------------
class PaymentScheduleItemInline(admin.TabularInline):
    model = PaymentScheduleItem
    extra = 1
    fields = ("label", "amount", "due_date", "order")


@admin.register(EducationalContent)
class EducationalContentAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "agreement_number", "company_name",
        "estimated_cost", "budget_type", "is_hidden", "created_at",
    )
    list_filter = ("type", "budget_type", "is_hidden", "payment_method")
    search_fields = ("name", "agreement_number", "company_name", "subject")
    readonly_fields = ("stored_name", "created_at", "updated_at")
    inlines = [PaymentScheduleItemInline]


@admin.register(PaymentScheduleItem)
class PaymentScheduleItemAdmin(admin.ModelAdmin):
    list_display = ("id", "content", "label", "amount", "due_date", "order")
    list_filter = ("due_date",)
    search_fields = ("label",)


# ---------------- NafathCenterAgreement ----------------
class PaymentScheduleRowInline(admin.TabularInline):
    model = PaymentScheduleRow
    extra = 1
    fields = ("label", "amount", "due_date", "order")
    ordering = ("order", "id")


@admin.register(NafathCenterAgreement)
class NafathCenterAgreementAdmin(admin.ModelAdmin):
    list_display = (
        "id", "agreement_number", "name", "company_name",
        "estimated_cost", "budget_type", "payment_method","payment_text",
        "start_date", "end_date", "is_hidden", "created_at",
    )
    list_filter = (
        "type", "budget_type", "payment_method", "is_hidden",
        "start_date", "end_date",
    )
    search_fields = ("name", "agreement_number", "company_name", "subject")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    inlines = [PaymentScheduleRowInline]


@admin.register(PaymentScheduleRow)
class PaymentScheduleRowAdmin(admin.ModelAdmin):
    list_display = ("id", "agreement", "label", "amount", "due_date", "order")
    list_filter = ("due_date",)
    search_fields = ("label",)
    autocomplete_fields = ("agreement",)
    ordering = ("agreement", "order", "id")