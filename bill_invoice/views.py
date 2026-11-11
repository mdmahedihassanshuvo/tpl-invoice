from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from decimal import Decimal
from .forms import VoucherForm, VoucherLineFormSet
from .models import Voucher

def create(request):
    voucher = Voucher()
    form = VoucherForm(request.POST or None, request.FILES or None, instance=voucher)
    lines = VoucherLineFormSet(request.POST or None, instance=voucher, prefix='lines')
    if request.method == 'POST' and form.is_valid() and lines.is_valid():
        voucher = form.save()
        lines.instance = voucher
        lines.save()
        return redirect('bill_invoice:detail', pk=voucher.pk)
    return render(request, 'bill_invoice/form.html', {'form':form, 'lines':lines})

def detail(request, pk):
    voucher = get_object_or_404(Voucher, pk=pk)
    rows = list(voucher.lines.all())
    return render(request, 'bill_invoice/detail.html', {
        'voucher': voucher,
        'total_debit': sum((row.debit for row in rows), Decimal('0.00')),
        'total_credit': sum((row.credit for row in rows), Decimal('0.00')),
    })

def markdown(request, pk):
    v = get_object_or_404(Voucher, pk=pk)
    esc = lambda x: str(x or '').replace('|', r'\|').replace('\n', ' ')
    rows = ['# Payment Voucher', '', f'**Tiger Park Limited**  ', '2-16, Pallabi, Mirpur, Dhaka-1216, Bangladesh.  ', 'Cell: 01517327315', '', f'**Date:** {v.date}  ', f'**Voucher No:** {esc(v.voucher_no)}  ', f'**Department:** {esc(v.department)}  ', f'**Bank:** {esc(v.bank)}  ', f'**Ledger No:** {esc(v.ledger_no)}  ', f'**Cheque No:** {esc(v.cheque_no)}  ', f'**Cash:** {esc(v.cash)}  ', f'**Pay To:** {esc(v.pay_to)}', '', '| Date | Payment Method | Ref No | Description | Dr (BDT) | Cr (BDT) | Sign |', '|---|---|---|---|---:|---:|---|']
    for line in v.lines.all(): rows.append(f'| {line.date or ""} | {esc(line.payment_method)} | {esc(line.ref_no)} | {esc(line.description)} | {line.debit:.2f} | {line.credit:.2f} | {esc(line.signature)} |')
    rows += ['', f'**Total Dr:** {sum((x.debit for x in v.lines.all()), start=0):.2f} BDT  ', f'**Total Cr:** {sum((x.credit for x in v.lines.all()), start=0):.2f} BDT  ', f'**Amount in Words:** {esc(v.amount_words)}', '', f'Prepared by: {esc(v.prepared_by)} | Received by: {esc(v.received_by)} | Checked by: {esc(v.checked_by)} | Approved by: {esc(v.approved_by)}']
    response = HttpResponse('\n'.join(rows), content_type='text/markdown; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="voucher-{v.pk}.md"'
    return response
