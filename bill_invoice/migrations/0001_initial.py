from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('voucher_no', models.CharField(blank=True, max_length=40)),
                ('department', models.CharField(blank=True, max_length=120)),
                ('bank', models.CharField(blank=True, max_length=120)),
                ('ledger_no', models.CharField(blank=True, max_length=80)),
                ('cheque_no', models.CharField(blank=True, max_length=80)),
                ('cash', models.CharField(blank=True, max_length=80)),
                ('pay_to', models.CharField(blank=True, max_length=200)),
                ('amount_words', models.CharField(blank=True, max_length=300)),
                ('prepared_by', models.CharField(blank=True, max_length=120)),
                ('received_by', models.CharField(blank=True, max_length=120)),
                ('checked_by', models.CharField(blank=True, max_length=120)),
                ('approved_by', models.CharField(blank=True, max_length=120)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='VoucherLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('payment_method', models.CharField(blank=True, max_length=80)),
                ('ref_no', models.CharField(blank=True, max_length=80)),
                ('description', models.CharField(blank=True, max_length=300)),
                ('debit', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('credit', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('signature', models.CharField(blank=True, max_length=120)),
                ('voucher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lines', to='bill_invoice.voucher')),
            ],
        ),
    ]
