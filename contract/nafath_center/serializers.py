from rest_framework import serializers
from .models import NafathCenterAgreement


class PaymentScheduleItemSerializer(serializers.Serializer):
    label = serializers.CharField(allow_blank=True, required=False, default='')
    amount = serializers.DecimalField(max_digits=14, decimal_places=2, default=0)
    dueDate = serializers.DateField(required=False, allow_null=True, default=None)


class NafathCenterAgreementSerializer(serializers.ModelSerializer):
    # Accept camelCase from frontend, map to snake_case model fields.
    agreementNumber = serializers.CharField(source='agreement_number')
    companyName = serializers.CharField(source='company_name')
    estimatedCost = serializers.DecimalField(
        source='estimated_cost', max_digits=14, decimal_places=2, required=False, default=0
    )
    startDate = serializers.DateField(
        source='start_date', required=False, allow_null=True
    )
    endDate = serializers.DateField(
        source='end_date', required=False, allow_null=True
    )
    paymentMethod = serializers.CharField(
        source='payment_method', required=False, allow_blank=True
    )
    paymentText = serializers.CharField(
        source='payment_text', required=False, allow_blank=True
    )
    paymentSchedule = PaymentScheduleItemSerializer(
        source='payment_schedule', many=True, required=False
    )
    budgetType = serializers.CharField(
        source='budget_type', required=False, allow_blank=True
    )
    isHidden = serializers.BooleanField(source='is_hidden', required=False, default=False)
    fileName = serializers.CharField(
        source='file_name', required=False, allow_blank=True
    )
    file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = NafathCenterAgreement
        fields = [
            'id',
            'type',
            'agreementNumber',
            'name',
            'companyName',
            'subject',
            'estimatedCost',
            'startDate',
            'endDate',
            'paymentMethod',
            'paymentText',
            'paymentSchedule',
            'status',
            'disbursement',
            'budgetType',
            'isHidden',
            'fileName',
            'file',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    # ---------- paymentSchedule normalisation ----------
    def to_internal_value(self, data):
        """
        Accept `paymentSchedule` either as:
          - a real JSON array (application/json), OR
          - a JSON-encoded string (multipart/FormData).
        """
        # Work on a mutable copy because QueryDict is immutable.
        if hasattr(data, 'dict'):
            data = data.dict()

        raw = data.get('paymentSchedule')
        if isinstance(raw, str) and raw.strip():
            import json
            try:
                data['paymentSchedule'] = json.loads(raw)
            except json.JSONDecodeError:
                raise serializers.ValidationError({
                    'paymentSchedule': 'Invalid JSON string.'
                })
        elif raw in ('', None):
            data.pop('paymentSchedule', None)

        return super().to_internal_value(data)

    # ---------- output shape (camelCase) ----------
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Rename `file` URL if any
        if instance.file:
            request = self.context.get('request')
            url = instance.file.url
            rep['fileUrl'] = request.build_absolute_uri(url) if request else url
        else:
            rep['fileUrl'] = None
        return rep