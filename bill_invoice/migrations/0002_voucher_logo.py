from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('bill_invoice', '0001_initial')]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='logo',
            field=models.FileField(blank=True, upload_to='voucher_logos/'),
        ),
    ]
