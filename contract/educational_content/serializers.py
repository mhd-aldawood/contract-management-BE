# educational_contents/serializers.py
from rest_framework import serializers
from .models import EducationalContent, PaymentScheduleItem

import json
class FlexibleDateField(serializers.DateField):
    def to_internal_value(self, value):
        if value in ("", None):
            return None
        return super().to_internal_value(value)

class PaymentScheduleItemSerializer(serializers.ModelSerializer):
    dueDate = FlexibleDateField(source="due_date", required=False, allow_null=True)

    class Meta:
        model = PaymentScheduleItem
        fields = ["id", "label", "amount", "dueDate", "order"]


class EducationalContentSerializer(serializers.ModelSerializer):
    agreementNumber   = serializers.CharField(source="agreement_number", required=False, allow_blank=True)
    companyName       = serializers.CharField(source="company_name", required=False, allow_blank=True)
    additionalCourses = serializers.CharField(source="additional_courses", required=False, allow_blank=True)
    estimatedCost     = serializers.DecimalField(source="estimated_cost", max_digits=14, decimal_places=2, required=False)
    startDate         = serializers.DateField(source="start_date", required=False, allow_null=True)
    endDate           = serializers.DateField(source="end_date", required=False, allow_null=True)
    paymentMethod     = serializers.CharField(source="payment_method", required=False, allow_blank=True)
    paymentText       = serializers.CharField(source="payment_text", required=False, allow_blank=True)
    quarterlyDue      = serializers.DecimalField(source="quarterly_due", max_digits=14, decimal_places=2, required=False)
    budgetType        = serializers.CharField(source="budget_type", required=False)
    contractText      = serializers.CharField(source="contract_text", required=False, allow_blank=True)
    isHidden          = serializers.BooleanField(source="is_hidden", required=False)
    fileName          = serializers.CharField(source="original_name", required=False, allow_blank=True)
    storedName        = serializers.CharField(source="stored_name", read_only=True)
    fileUrl           = serializers.SerializerMethodField(read_only=True)
    file              = serializers.FileField(required=False, allow_null=True, write_only=True)


    paymentSchedule = PaymentScheduleItemSerializer(many=True, required=False)

    class Meta:
        model = EducationalContent
        fields = [
            "id", "type",
            "agreementNumber", "name", "companyName", "subject",
            "additionalCourses", "estimatedCost", "startDate", "endDate",
            "paymentMethod", "paymentText", "paymentSchedule", "quarterlyDue",
            "status", "disbursement", "budgetType", "contractText",
            "isHidden", "fileName", "storedName", "fileUrl", "file",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "fileUrl", "storedName"]

    def get_fileUrl(self, obj):
        if not obj.file:
            return ""
        request = self.context.get("request")
        url = obj.file.url
        return request.build_absolute_uri(url) if request else url

    def create(self, validated_data):
        schedule_data = validated_data.pop("paymentSchedule", [])
        instance = EducationalContent.objects.create(**validated_data)
        for i, item in enumerate(schedule_data):
            PaymentScheduleItem.objects.create(
                content=instance,
                label=item.get("label", ""),
                amount=item.get("amount", 0) or 0,
                due_date=item.get("due_date"),
                order=i,
            )
        return instance

    def update(self, instance, validated_data):
        schedule_data = validated_data.pop("paymentSchedule", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if schedule_data is not None:
            instance.payment_schedule.all().delete()
            self._save_schedule(instance, schedule_data)
        return instance

    def _save_schedule(self, instance, schedule_data):
        for i, item in enumerate(schedule_data):
            PaymentScheduleItem.objects.create(
                content=instance,
                label=item.get("label", ""),
                amount=item.get("amount", 0),
                due_date=item.get("due_date"),
                order=i,
            )
    def to_internal_value(self, data):
        # multipart: paymentSchedule arrives as a JSON string
        data = data.dict() if hasattr(data, "dict") else dict(data)
        v = data.get("paymentSchedule")
        if isinstance(v, str):
            try:
                data["paymentSchedule"] = json.loads(v)
            except json.JSONDecodeError:
                data.pop("paymentSchedule", None)
        return super().to_internal_value(data)

    def get_fileUrl(self, obj):
        if not obj.file:
            return ""
        request = self.context.get("request")
        url = obj.file.url
        return request.build_absolute_uri(url) if request else url