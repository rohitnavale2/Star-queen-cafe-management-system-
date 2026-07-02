from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('category', models.CharField(choices=[
                    ('ice_cream', 'Ice Cream Sundaes'),
                    ('milkshakes', 'Milkshakes'),
                    ('cold_coffee', 'Cold Coffee'),
                    ('pizza', 'Pizza'),
                    ('burgers', 'Burgers'),
                    ('momos', 'Momos'),
                    ('french_fries', 'French Fries'),
                    ('fresh_juices', 'Fresh Juices'),
                    ('smoothies', 'Smoothies'),
                    ('lassi', 'Lassi'),
                    ('falooda', 'Falooda'),
                ], max_length=50)),
                ('is_available', models.BooleanField(default=True)),
                ('is_bestseller', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['category', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('guests', models.PositiveIntegerField()),
                ('special_request', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[
                    ('pending', 'Pending'),
                    ('confirmed', 'Confirmed'),
                    ('cancelled', 'Cancelled'),
                ], default='pending', max_length=20)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[
                    ('interior', 'Cafe Interior'),
                    ('food', 'Food Images'),
                    ('customers', 'Customer Photos'),
                ], max_length=20)),
                ('image_url', models.URLField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
