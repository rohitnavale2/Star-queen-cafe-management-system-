from django.db import models


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
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
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    is_available = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()}) - ₹{self.price}"


class Reservation(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()
    special_request = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time} ({self.guests} guests)"


class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('interior', 'Cafe Interior'),
        ('food', 'Food Images'),
        ('customers', 'Customer Photos'),
    ]
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text='Optional: use URL if not uploading a file')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    def get_image(self):
        """Returns uploaded image or fallback URL"""
        if self.image:
            return self.image.url
        return self.image_url or ''


# ═══════════════════════════════════════════
#  HOME DELIVERY SYSTEM
# ═══════════════════════════════════════════

class DeliveryOrder(models.Model):
    STATUS_CHOICES = [
        ('pending',    'Order Placed'),
        ('confirmed',  'Confirmed'),
        ('preparing',  'Preparing'),
        ('picked_up',  'Picked Up by Delivery'),
        ('on_the_way', 'On the Way'),
        ('delivered',  'Delivered'),
        ('cancelled',  'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('cod',  'Cash on Delivery'),
        ('upi',  'UPI / QR Code'),
        ('card', 'Card on Delivery'),
    ]

    # Customer details
    name        = models.CharField(max_length=100)
    phone       = models.CharField(max_length=15)
    email       = models.EmailField(blank=True)
    address     = models.TextField()
    landmark    = models.CharField(max_length=200, blank=True)
    pincode     = models.CharField(max_length=10)

    # Order meta
    order_number   = models.CharField(max_length=20, unique=True)
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cod')
    special_note   = models.TextField(blank=True)

    # Pricing
    subtotal        = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=30)
    discount        = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total           = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    # Timestamps
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    delivered_at  = models.DateTimeField(null=True, blank=True)

    # Estimated delivery time (minutes)
    estimated_time = models.PositiveIntegerField(default=40)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.order_number} — {self.name} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if not self.order_number:
            import random, string
            self.order_number = 'SQC' + ''.join(random.choices(string.digits, k=6))
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order     = models.ForeignKey(DeliveryOrder, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity  = models.PositiveIntegerField(default=1)
    price     = models.DecimalField(max_digits=6, decimal_places=2)  # price at time of order

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"

    @property
    def line_total(self):
        return self.price * self.quantity


class DeliveryArea(models.Model):
    area_name       = models.CharField(max_length=100)
    pincode         = models.CharField(max_length=10)
    delivery_charge = models.DecimalField(max_digits=6, decimal_places=2, default=30)
    is_available    = models.BooleanField(default=True)
    min_order       = models.DecimalField(max_digits=6, decimal_places=2, default=100)

    def __str__(self):
        return f"{self.area_name} ({self.pincode}) — ₹{self.delivery_charge}"


class CafeSettings(models.Model):
    """Single row settings table — QR code, UPI ID, etc."""

    # UPI / Payment
    upi_id          = models.CharField(max_length=100, blank=True, help_text="e.g. rohit@upi or 9876543210@paytm")
    upi_name        = models.CharField(max_length=100, blank=True, help_text="Name shown on payment screen")
    qr_code         = models.ImageField(upload_to='qr/', blank=True, null=True, help_text="Upload your UPI QR code image")
    payment_note    = models.CharField(max_length=200, blank=True, default="Scan & Pay — UPI / GPay / PhonePe / Paytm")

    # Razorpay Keys
    razorpay_key_id     = models.CharField(max_length=100, blank=True, help_text="Razorpay Key ID (rzp_test_...)")
    razorpay_key_secret = models.CharField(max_length=100, blank=True, help_text="Razorpay Key Secret")
    razorpay_enabled    = models.BooleanField(default=False, help_text="Enable online payment via Razorpay")

    # Cafe basic info
    cafe_name       = models.CharField(max_length=100, default="Star Queen Cafe")
    cafe_phone      = models.CharField(max_length=15, blank=True)
    cafe_address    = models.TextField(blank=True)
    cafe_email      = models.EmailField(blank=True, help_text="For sending receipts to customers")

    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Cafe Settings"
        verbose_name_plural = "Cafe Settings"

    def __str__(self):
        return "Star Queen Cafe Settings"

    def save(self, *args, **kwargs):
        # Only one row allowed
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Payment(models.Model):
    """Razorpay payment record"""

    STATUS_CHOICES = [
        ('created',  'Created'),
        ('pending',  'Pending'),
        ('success',  'Success'),
        ('failed',   'Failed'),
        ('refunded', 'Refunded'),
    ]

    order             = models.OneToOneField(DeliveryOrder, on_delete=models.CASCADE, related_name='payment')
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    razorpay_signature  = models.CharField(max_length=200, blank=True)
    amount            = models.DecimalField(max_digits=8, decimal_places=2)
    currency          = models.CharField(max_length=10, default='INR')
    status            = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')
    created_at        = models.DateTimeField(auto_now_add=True)
    paid_at           = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment for Order #{self.order.order_number} — {self.get_status_display()}"
