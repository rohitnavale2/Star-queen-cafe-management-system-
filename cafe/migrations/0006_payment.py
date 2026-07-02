from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0005_cafe_settings'),
    ]

    operations = [
        # Add Razorpay fields to CafeSettings
        migrations.AddField(
            model_name='cafesettings',
            name='razorpay_key_id',
            field=models.CharField(blank=True, max_length=100, help_text='Razorpay Key ID (rzp_test_...)'),
        ),
        migrations.AddField(
            model_name='cafesettings',
            name='razorpay_key_secret',
            field=models.CharField(blank=True, max_length=100, help_text='Razorpay Key Secret'),
        ),
        migrations.AddField(
            model_name='cafesettings',
            name='razorpay_enabled',
            field=models.BooleanField(default=False, help_text='Enable online payment via Razorpay'),
        ),
        migrations.AddField(
            model_name='cafesettings',
            name='cafe_email',
            field=models.EmailField(blank=True, help_text='For sending receipts to customers'),
        ),
        # Create Payment model
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razorpay_order_id',   models.CharField(max_length=100, unique=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=100)),
                ('razorpay_signature',  models.CharField(blank=True, max_length=200)),
                ('amount',    models.DecimalField(decimal_places=2, max_digits=8)),
                ('currency',  models.CharField(default='INR', max_length=10)),
                ('status',    models.CharField(choices=[
                    ('created', 'Created'), ('pending', 'Pending'),
                    ('success', 'Success'), ('failed', 'Failed'), ('refunded', 'Refunded'),
                ], default='created', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('paid_at',    models.DateTimeField(blank=True, null=True)),
                ('order', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='payment',
                    to='cafe.deliveryorder',
                )),
            ],
        ),
    ]
