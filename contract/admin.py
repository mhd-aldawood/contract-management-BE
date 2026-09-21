from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .educational_content.models import EducationalContent, PaymentScheduleItem


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