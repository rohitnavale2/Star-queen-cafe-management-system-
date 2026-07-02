from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0002_sample_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_name', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=10)),
                ('delivery_charge', models.DecimalField(decimal_places=2, default=30, max_digits=6)),
                ('is_available', models.BooleanField(default=True)),
                ('min_order', models.DecimalField(decimal_places=2, default=100, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(blank=True)),
                ('address', models.TextField()),
                ('landmark', models.CharField(blank=True, max_length=200)),
                ('pincode', models.CharField(max_length=10)),
                ('order_number', models.CharField(max_length=20, unique=True)),
                ('status', models.CharField(choices=[
                    ('pending', 'Order Placed'),
                    ('confirmed', 'Confirmed'),
                    ('preparing', 'Preparing'),
                    ('picked_up', 'Picked Up by Delivery'),
                    ('on_the_way', 'On the Way'),
                    ('delivered', 'Delivered'),
                    ('cancelled', 'Cancelled'),
                ], default='pending', max_length=20)),
                ('payment_method', models.CharField(choices=[
                    ('cod', 'Cash on Delivery'),
                    ('upi', 'UPI / QR Code'),
                    ('card', 'Card on Delivery'),
                ], default='cod', max_length=10)),
                ('special_note', models.TextField(blank=True)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('delivery_charge', models.DecimalField(decimal_places=2, default=30, max_digits=6)),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('delivered_at', models.DateTimeField(blank=True, null=True)),
                ('estimated_time', models.PositiveIntegerField(default=40)),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='cafe.deliveryorder')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafe.menuitem')),
            ],
        ),
        migrations.RunPython(
            lambda apps, schema_editor: apps.get_model('cafe', 'DeliveryArea').objects.bulk_create([
                apps.get_model('cafe', 'DeliveryArea')(area_name='Beed City', pincode='431122', delivery_charge=20, min_order=80, is_available=True),
                apps.get_model('cafe', 'DeliveryArea')(area_name='DP Road Area', pincode='431123', delivery_charge=25, min_order=100, is_available=True),
                apps.get_model('cafe', 'DeliveryArea')(area_name='Beed Naka', pincode='431124', delivery_charge=30, min_order=100, is_available=True),
                apps.get_model('cafe', 'DeliveryArea')(area_name='Georai', pincode='431127', delivery_charge=50, min_order=150, is_available=True),
            ]),
            lambda apps, schema_editor: None,
        ),
    ]
