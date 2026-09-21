# educational_contents/models.py
import uuid
import os
from django.db import models
from django.utils import timezone


def upload_to_path(instance, filename):
    """
    Store files under media/educational_contents/<year>/<month>/<uuid>.<ext>
    and keep the original filename on the instance.
    """
    ext = os.path.splitext(filename)[1].lower()
    new_name = f"{uuid.uuid4().hex}{ext}"
    now = timezone.now()
    return f"educational_contents/{now.year}/{now.month:02d}/{new_name}"


class EducationalContent(models.Model):
    TYPE_CHOICES = [("educational-content", "Educational Content")]
    BUDGET_TYPE_CHOICES = [("current", "Current"), ("investment", "Investment")]
    PAYMENT_METHOD_CHOICES = [("text", "Text"), ("table", "Table"), ("", "None")]

    type = models.CharField(max_length=64, choices=TYPE_CHOICES, default="educational-content")

    agreement_number = models.CharField(max_length=100, blank=True, default="")
    name = models.CharField(max_length=255, blank=True, default="")
    company_name = models.CharField(max_length=255, blank=True, default="")
    subject = models.CharField(max_length=255, blank=True, default="")
    additional_courses = models.TextField(blank=True, default="")
    estimated_cost = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    payment_method = models.CharField(max_length=16, choices=PAYMENT_METHOD_CHOICES, blank=True, default="")
    payment_text = models.TextField(blank=True, default="")
    quarterly_due = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    status = models.CharField(max_length=255, blank=True, default="")
    disbursement = models.CharField(max_length=255, blank=True, default="")
    budget_type = models.CharField(max_length=16, choices=BUDGET_TYPE_CHOICES, default="current")
    contract_text = models.TextField(blank=True, default="")
    is_hidden = models.BooleanField(default=False)

    # ---- file storage ----
    file = models.FileField(upload_to=upload_to_path, null=True, blank=True)
    original_name = models.CharField(max_length=255, blank=True, default="")  # user's original filename
    stored_name = models.CharField(max_length=255, blank=True, default="")    # uuid filename on disk

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "educational_contents"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name or f"EducationalContent #{self.pk}"


class PaymentScheduleItem(models.Model):
    content = models.ForeignKey(
        EducationalContent, related_name="payment_schedule", on_delete=models.CASCADE
    )
    label = models.CharField(max_length=255, blank=True, default="")
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    due_date = models.DateField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "educational_content_payment_schedule"
        ordering = ["order"]