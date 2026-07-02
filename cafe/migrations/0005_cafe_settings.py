from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0004_gallery_image_upload'),
    ]

    operations = [
        migrations.CreateModel(
            name='CafeSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upi_id',       models.CharField(blank=True, max_length=100, help_text='e.g. rohit@upi or 9876543210@paytm')),
                ('upi_name',     models.CharField(blank=True, max_length=100, help_text='Name shown on payment screen')),
                ('qr_code',      models.ImageField(blank=True, null=True, upload_to='qr/', help_text='Upload your UPI QR code image')),
                ('payment_note', models.CharField(blank=True, default='Scan & Pay — UPI / GPay / PhonePe / Paytm', max_length=200)),
                ('cafe_name',    models.CharField(default='Star Queen Cafe', max_length=100)),
                ('cafe_phone',   models.CharField(blank=True, max_length=15)),
                ('cafe_address', models.TextField(blank=True)),
                ('updated_at',   models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Cafe Settings',
                'verbose_name_plural': 'Cafe Settings',
            },
        ),
        migrations.RunPython(
            lambda apps, schema_editor: apps.get_model('cafe', 'CafeSettings').objects.create(
                pk=1,
                upi_id='yourname@upi',
                upi_name='Star Queen Cafe',
                payment_note='Scan & Pay — UPI / GPay / PhonePe / Paytm',
                cafe_name='Star Queen Cafe',
            ),
            lambda apps, schema_editor: None,
        ),
    ]
