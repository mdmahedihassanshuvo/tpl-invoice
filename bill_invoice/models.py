from django.db import models

class Voucher(models.Model):
    logo = models.FileField(upload_to='voucher_logos/', blank=True)
    date = models.DateField()
    voucher_no = models.CharField(max_length=40, blank=True)
    department = models.CharField(max_length=120, blank=True)
    bank = models.CharField(max_length=120, blank=True)
    ledger_no = models.CharField(max_length=80, blank=True)
    cheque_no = models.CharField(max_length=80, blank=True)
    cash = models.CharField(max_length=80, blank=True)
    pay_to = models.CharField(max_length=200, blank=True)
    amount_words = models.CharField(max_length=300, blank=True)
    prepared_by = models.CharField(max_length=120, blank=True)
    received_by = models.CharField(max_length=120, blank=True)
    checked_by = models.CharField(max_length=120, blank=True)
    approved_by = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.voucher_no or f'Voucher {self.pk}'

class VoucherLine(models.Model):
    voucher = models.ForeignKey(Voucher, related_name='lines', on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=80, blank=True)
    ref_no = models.CharField(max_length=80, blank=True)
    description = models.CharField(max_length=300, blank=True)
    debit = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    signature = models.CharField(max_length=120, blank=True)
