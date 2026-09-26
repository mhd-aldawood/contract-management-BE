
from django.db import models
from contract.helper import UploadToPath
from contract.models import PaymentScheduleRowBase


class LifeLongAgreement(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('text', 'Text'),
        ('table', 'Table'),
    ]
    BUDGET_TYPE_CHOICES = [
        ('current', 'Current'),
        ('budget', 'Budget'),
    ]

    # Core
    type = models.CharField(max_length=64, default='nafath-center')
    agreement_number = models.CharField(max_length=255, db_index=True)
    company_name = models.CharField(max_length=255)
    agreement_name = models.CharField(max_length=255)
    subject = models.TextField(blank=True, default='')

    # dates
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    # Payment
    payment_method = models.CharField(
        max_length=16, choices=PAYMENT_METHOD_CHOICES, blank=True, default=''
    )
    payment_text = models.TextField(blank=True, default='')

    # Status / meta
    status = models.CharField(max_length=255, blank=True, default='')
    disbursement = models.CharField(max_length=255, blank=True, default='')
    budget_type = models.CharField(
        max_length=16, choices=BUDGET_TYPE_CHOICES, default='current'
    )
    is_hidden = models.BooleanField(default=False)

    file = models.FileField(
        upload_to=UploadToPath('lifelong/files'),
        null=True,
        blank=True,
    )
    file_name = models.CharField(max_length=512, blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.agreement_number} — {self.name}'


class LifeLongAgreementPaymentRow(PaymentScheduleRowBase):
    agreement = models.ForeignKey(
        LifeLongAgreement,
        related_name='payment_schedule',
        on_delete=models.CASCADE,
    )