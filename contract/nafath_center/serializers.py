import json

from rest_framework import serializers
from .models import NafathCenterAgreement, PaymentScheduleRow


class PaymentScheduleRowSerializer(serializers.ModelSerializer):
    dueDate = serializers.DateField(
        source='due_date', required=False, allow_null=True
    )

    class Meta:
        model = PaymentScheduleRow
        # NOTE: field names here = wire names (camelCase)
        fields = ['id', 'label', 'amount', 'dueDate', 'order']
        read_only_fields = ['id']

    def validate_amount(self, value):
        if value is None or value <= 0:
            raise serializers.ValidationError('المبلغ يجب أن يكون أكبر من صفر')
        return value


class NafathCenterAgreementSerializer(serializers.ModelSerializer):
    # ---- nested rows: wire key "paymentSchedule" → model attr "payment_schedule"
    payment_schedule  = PaymentScheduleRowSerializer(
        many=True,
        required=False,
        allow_null=True,
    )

    # ---- camelCase wire names → snake_case model attrs
    agreementNumber   = serializers.CharField(source='agreement_number',   required=False, allow_blank=True)
    companyName       = serializers.CharField(source='company_name',       required=False, allow_blank=True)
    estimatedCost     = serializers.DecimalField(source='estimated_cost', max_digits=14, decimal_places=2, required=False)
    startDate         = serializers.DateField(source='start_date',   required=False, allow_null=True)
    endDate           = serializers.DateField(source='end_date',     required=False, allow_null=True)
    paymentMethod     = serializers.CharField(source='payment_method', required=False, allow_blank=True)
    paymentText       = serializers.CharField(source='payment_text',   required=False, allow_blank=True)
    budgetType        = serializers.CharField(source='budget_type',    required=False, allow_blank=True)
    isHidden          = serializers.BooleanField(source='is_hidden',   required=False)
    fileName          = serializers.CharField(source='file_name',      required=False, allow_blank=True)

    class Meta:
        model = NafathCenterAgreement
        # list every wire field you want exposed
        fields = [
            'id', 'type', 'agreementNumber', 'name', 'companyName', 'subject',
             'estimatedCost', 'startDate', 'endDate',
            'paymentMethod', 'paymentText', 'payment_schedule',
            'status', 'disbursement', 'budgetType',
            'isHidden', 'fileName', 'file',
        ]
        read_only_fields = ['id']

    # ------------------------------------------------------------------
    # Handle BOTH JSON and multipart/form-data clients
    # ------------------------------------------------------------------
    def to_internal_value(self, data):
        print('>>> to_internal_value CALLED, type:', type(data))
        print('>>> raw keys:', list(data.keys()) if hasattr(data, 'keys') else data)
        # 1. QueryDict (multipart / urlencoded) -> plain dict
        if hasattr(data, 'dict'):
            data = data.dict()
        print('>>> after .dict():', data)

        # 2. Remap camelCase wire key -> snake_case serializer field
        if 'paymentSchedule' in data:
            data['payment_schedule'] = data.pop('paymentSchedule')
            print('>>> remapped paymentSchedule -> payment_schedule')
        else:
            print('>>> NO paymentSchedule KEY FOUND')

        # 3. If the client sent the list as a JSON string, decode it
        raw = data.get('payment_schedule')
        if isinstance(raw, str):
            try:
                data['payment_schedule'] = json.loads(raw)
                print('>>> decoded JSON string ->', data['payment_schedule'])
            except Exception as e:
                print('>>> json.loads failed:', e)

        # 4. Boolean-ish string coercion for multipart ("true"/"false")
        if isinstance(data.get('isHidden'), str):
            data['isHidden'] = data['isHidden'].lower() in ('1', 'true', 'yes', 'on')

        return super().to_internal_value(data)

    def create(self, validated_data):
        print('VALIDATED KEYS:', list(validated_data.keys()))  # ← add this
        print('ROWS RECEIVED:', validated_data.get('payment_schedule'))

        rows = validated_data.pop('payment_schedule', None) or []
        agreement = NafathCenterAgreement.objects.create(**validated_data)
        self._save_rows(agreement, rows)
        return agreement

    def update(self, instance, validated_data):
        rows = validated_data.pop('payment_schedule', None)
        instance = super().update(instance, validated_data)
        if rows is not None:
            instance.payment_schedule.all().delete()
            self._save_rows(instance, rows)
        return instance

    @staticmethod
    def _save_rows(agreement, rows):
        PaymentScheduleRow.objects.bulk_create([
            PaymentScheduleRow(
                agreement=agreement,
                label=row.get('label') or '',
                amount=row['amount'],
                due_date=row.get('due_date'),
                order=i,
            )
            for i, row in enumerate(rows)
        ])