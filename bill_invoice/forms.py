from django import forms
from django.forms import inlineformset_factory
from decimal import Decimal
from django.core.exceptions import ValidationError
from .models import Voucher, VoucherLine

class VoucherForm(forms.ModelForm):
    def clean_logo(self):
        logo = self.cleaned_data['logo']
        if logo:
            if logo.size > 5 * 1024 * 1024:
                raise ValidationError('Logo must be 5 MB or smaller.')
            signature = logo.read(12)
            logo.seek(0)
            if not (signature.startswith(b'\x89PNG\r\n\x1a\n') or signature.startswith(b'\xff\xd8\xff')):
                raise ValidationError('Upload a PNG or JPEG logo.')
        return logo
    class Meta:
        model = Voucher
        fields = '__all__'
        exclude = ('created_at',)
        widgets = {'date': forms.DateInput(attrs={'type': 'date', 'class': 'voucher-date', 'onclick': 'if (this.showPicker) this.showPicker()'})}

class VoucherLineForm(forms.ModelForm):
    debit = forms.DecimalField(required=False, max_digits=14, decimal_places=2)
    credit = forms.DecimalField(required=False, max_digits=14, decimal_places=2)

    class Meta:
        model = VoucherLine
        exclude = ('voucher',)
        widgets = {'date': forms.DateInput(attrs={'type': 'date', 'class': 'voucher-date', 'onclick': 'if (this.showPicker) this.showPicker()'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_bound and not self.instance.pk:
            self.instance.debit = None
            self.instance.credit = None
            self.initial['debit'] = None
            self.initial['credit'] = None

    def clean_debit(self):
        return self.cleaned_data['debit'] or Decimal('0')

    def clean_credit(self):
        return self.cleaned_data['credit'] or Decimal('0')

VoucherLineFormSet = inlineformset_factory(Voucher, VoucherLine, form=VoucherLineForm, extra=1, can_delete=True)
