from django.contrib import admin
from django.utils.html import format_html
from .models import MenuItem, Reservation, GalleryImage, DeliveryOrder, OrderItem, DeliveryArea, CafeSettings, Payment


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'is_bestseller']
    list_filter = ['category', 'is_available', 'is_bestseller']
    search_fields = ['name']
    list_editable = ['price', 'is_available', 'is_bestseller']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'date', 'time', 'guests', 'status', 'created_at']
    list_filter = ['status', 'date']
    search_fields = ['name', 'phone']
    list_editable = ['status']


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'image_preview', 'created_at']
    list_filter  = ['category']
    search_fields = ['title']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        url = obj.get_image()
        if url:
            return format_html(
                '<img src="{}" style="width:80px;height:60px;object-fit:cover;border:1px solid #c9a84c;" />',
                url
            )
        return '— No Image —'
    image_preview.short_description = 'Preview'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['menu_item', 'quantity', 'price', 'get_line_total']
    fields = ['menu_item', 'quantity', 'price', 'get_line_total']

    def get_line_total(self, obj):
        return f"₹{obj.line_total}"
    get_line_total.short_description = 'Line Total'


@admin.register(DeliveryOrder)
class DeliveryOrderAdmin(admin.ModelAdmin):
    # ✅ 'status' must appear in list_display before list_editable can use it
    list_display = [
        'order_number', 'name', 'phone',
        'status',           # <-- plain 'status' field (editable)
        'status_colored',   # <-- colored badge (read-only display)
        'total', 'payment_method', 'created_at'
    ]
    list_filter  = ['status', 'payment_method', 'created_at']
    search_fields = ['order_number', 'name', 'phone']
    list_editable = ['status']   # ✅ works because 'status' is in list_display
    readonly_fields = ['order_number', 'subtotal', 'delivery_charge', 'total', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    ordering = ['-created_at']

    fieldsets = (
        ('Order Info', {
            'fields': ('order_number', 'status', 'estimated_time')
        }),
        ('Customer Details', {
            'fields': ('name', 'phone', 'email', 'address', 'landmark', 'pincode')
        }),
        ('Payment & Pricing', {
            'fields': ('payment_method', 'subtotal', 'delivery_charge', 'discount', 'total')
        }),
        ('Notes', {
            'fields': ('special_note',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'delivered_at')
        }),
    )

    def status_colored(self, obj):
        colors = {
            'pending':    '#f0a500',
            'confirmed':  '#17a2b8',
            'preparing':  '#6f42c1',
            'picked_up':  '#fd7e14',
            'on_the_way': '#007bff',
            'delivered':  '#28a745',
            'cancelled':  '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;'
            'border-radius:12px;font-size:11px;font-weight:600;">{}</span>',
            color, obj.get_status_display()
        )
    status_colored.short_description = 'Status Label'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'menu_item', 'quantity', 'price']
    list_filter  = ['menu_item__category']


@admin.register(DeliveryArea)
class DeliveryAreaAdmin(admin.ModelAdmin):
    list_display = ['area_name', 'pincode', 'delivery_charge', 'min_order', 'is_available']
    list_editable = ['delivery_charge', 'min_order', 'is_available']


@admin.register(CafeSettings)
class CafeSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('🚀 Razorpay Online Payment', {
            'fields': ('razorpay_enabled', 'razorpay_key_id', 'razorpay_key_secret'),
            'description': '⚡ Enable this for real GPay/PhonePe/UPI/Card payments. Get keys from razorpay.com → Settings → API Keys',
        }),
        ('💳 UPI / QR Payment (Manual)', {
            'fields': ('upi_id', 'upi_name', 'qr_code', 'qr_preview', 'payment_note'),
            'description': 'Shown when customer selects UPI payment (backup QR display).',
        }),
        ('🏪 Cafe Info', {
            'fields': ('cafe_name', 'cafe_phone', 'cafe_email', 'cafe_address'),
        }),
    )
    readonly_fields = ['qr_preview', 'updated_at']

    def qr_preview(self, obj):
        if obj.qr_code:
            return format_html(
                '<img src="{}" style="width:200px;height:200px;object-fit:contain;border:2px solid #c9a84c;padding:8px;" />',
                obj.qr_code.url
            )
        return '— No QR Code uploaded yet —'
    qr_preview.short_description = 'QR Preview'

    def has_add_permission(self, request):
        # Only one settings row allowed
        return not CafeSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display  = ['order', 'amount', 'status_badge', 'razorpay_payment_id', 'created_at', 'paid_at']
    list_filter   = ['status', 'created_at']
    search_fields = ['order__order_number', 'razorpay_payment_id', 'order__name']
    readonly_fields = ['order', 'razorpay_order_id', 'razorpay_payment_id',
                       'razorpay_signature', 'amount', 'currency', 'created_at', 'paid_at']
    ordering = ['-created_at']

    def status_badge(self, obj):
        colors = {
            'created':  '#17a2b8',
            'pending':  '#f0a500',
            'success':  '#28a745',
            'failed':   '#dc3545',
            'refunded': '#6c757d',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:600;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Payment Status'

    def has_add_permission(self, request):
        return False
