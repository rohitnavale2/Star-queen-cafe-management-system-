import json
import hmac
import hashlib
import razorpay
from decimal import Decimal
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from .models import MenuItem, GalleryImage, DeliveryOrder, OrderItem, DeliveryArea, CafeSettings, Payment
from .forms import ReservationForm, DeliveryOrderForm


CATEGORY_EMOJIS = {
    'ice_cream':    ('🍨', 'Ice Cream'),
    'milkshakes':   ('🥤', 'Milkshakes'),
    'cold_coffee':  ('☕', 'Cold Coffee'),
    'pizza':        ('🍕', 'Pizza'),
    'burgers':      ('🍔', 'Burgers'),
    'momos':        ('🥟', 'Momos'),
    'french_fries': ('🍟', 'French Fries'),
    'fresh_juices': ('🍊', 'Fresh Juices'),
    'smoothies':    ('🫐', 'Smoothies'),
    'lassi':        ('🥛', 'Lassi'),
    'falooda':      ('🌹', 'Falooda'),
}


# ── Helper ──────────────────────────────────────────────
def get_razorpay_client():
    settings = CafeSettings.get_settings()
    if settings.razorpay_key_id and settings.razorpay_key_secret:
        return razorpay.Client(auth=(settings.razorpay_key_id, settings.razorpay_key_secret))
    return None


def build_category_data():
    category_data = {}
    for cat_key, cat_name in MenuItem.CATEGORY_CHOICES:
        items = MenuItem.objects.filter(category=cat_key, is_available=True)
        if items.exists():
            emoji, label = CATEGORY_EMOJIS.get(cat_key, ('🍽️', cat_name))
            category_data[cat_name] = {'key': cat_key, 'items': items, 'emoji': emoji}
    return category_data


# ── Standard Pages ───────────────────────────────────────
def home(request):
    bestsellers = MenuItem.objects.filter(is_bestseller=True, is_available=True)[:6]
    categories_preview = [(emoji, label, key) for key, (emoji, label) in CATEGORY_EMOJIS.items()]
    return render(request, 'cafe/home.html', {
        'bestsellers': bestsellers,
        'categories_preview': categories_preview,
        'menu_categories': MenuItem.CATEGORY_CHOICES,
    })


def menu(request):
    selected_category = request.GET.get('category', '')
    category_data = {}
    for cat_key, cat_name in MenuItem.CATEGORY_CHOICES:
        if selected_category and selected_category != cat_key:
            continue
        items = MenuItem.objects.filter(category=cat_key, is_available=True)
        if items.exists():
            category_data[cat_name] = {'key': cat_key, 'items': items}
    return render(request, 'cafe/menu.html', {
        'category_data': category_data,
        'categories': MenuItem.CATEGORY_CHOICES,
        'selected_category': selected_category,
    })


def gallery(request):
    return render(request, 'cafe/gallery.html', {
        'interior_images':  GalleryImage.objects.filter(category='interior'),
        'food_images':      GalleryImage.objects.filter(category='food'),
        'customer_images':  GalleryImage.objects.filter(category='customers'),
        'food_placeholders': ['Cold Coffee', 'Pizza Slice', 'Mango Falooda', 'Veg Momos', 'Oreo Shake', 'French Fries'],
    })


def events(request):
    return render(request, 'cafe/events.html')


def visit(request):
    return render(request, 'cafe/visit.html')


def reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, f"Thank you, {obj.name}! Your table for {obj.guests} on {obj.date.strftime('%d %B %Y')} at {obj.time.strftime('%I:%M %p')} is confirmed.")
            return redirect('reservation')
        messages.error(request, "Please correct the errors below.")
    else:
        form = ReservationForm()
    return render(request, 'cafe/reservation.html', {'form': form})


# ═══════════════════════════════════════════════════════
#  HOME DELIVERY + RAZORPAY PAYMENT
# ═══════════════════════════════════════════════════════

def delivery_home(request):
    cafe_settings = CafeSettings.get_settings()
    return render(request, 'cafe/delivery.html', {
        'category_data': build_category_data(),
        'delivery_areas': DeliveryArea.objects.filter(is_available=True),
        'form': DeliveryOrderForm(),
        'cafe_settings': cafe_settings,
    })


def place_order(request):
    """
    Step 1: Validate cart + form
    Step 2: Create DeliveryOrder in DB
    Step 3a: If Razorpay enabled → create Razorpay order → go to payment page
    Step 3b: If COD/Card → confirm order directly
    """
    if request.method != 'POST':
        return redirect('delivery_home')

    form = DeliveryOrderForm(request.POST)
    cart_json = request.POST.get('cart_data', '[]')
    cafe_settings = CafeSettings.get_settings()

    try:
        cart_items = json.loads(cart_json)
    except (json.JSONDecodeError, ValueError):
        cart_items = []

    if not cart_items:
        messages.error(request, "Your cart is empty! Please add items before placing an order.")
        return redirect('delivery_home')

    if form.is_valid():
        order = form.save(commit=False)
        payment_method = request.POST.get('payment_method', 'cod')
        order.payment_method = payment_method

        # Calculate totals
        subtotal = Decimal('0')
        valid_items = []
        for ci in cart_items:
            try:
                item = MenuItem.objects.get(id=ci['id'], is_available=True)
                qty  = max(1, int(ci.get('qty', 1)))
                subtotal += item.price * qty
                valid_items.append((item, qty))
            except (MenuItem.DoesNotExist, KeyError, ValueError):
                continue

        if not valid_items:
            messages.error(request, "No valid items found in cart.")
            return redirect('delivery_home')

        # Delivery charge
        delivery_charge = Decimal('30')
        try:
            area = DeliveryArea.objects.get(pincode=order.pincode, is_available=True)
            delivery_charge = area.delivery_charge
            if subtotal < area.min_order:
                messages.error(request, f"Minimum order for {area.area_name} is ₹{area.min_order}.")
                return redirect('delivery_home')
        except DeliveryArea.DoesNotExist:
            pass

        order.subtotal        = subtotal
        order.delivery_charge = delivery_charge
        order.total           = subtotal + delivery_charge

        # For online payment — keep pending until payment confirmed
        if payment_method == 'upi' and cafe_settings.razorpay_enabled:
            order.status = 'pending'
        else:
            order.status = 'confirmed'

        order.save()

        # Save order items
        for item, qty in valid_items:
            OrderItem.objects.create(order=order, menu_item=item, quantity=qty, price=item.price)

        # ── RAZORPAY PAYMENT FLOW ──
        if payment_method == 'upi' and cafe_settings.razorpay_enabled:
            client = get_razorpay_client()
            if client:
                try:
                    amount_paise = int(order.total * 100)  # Razorpay uses paise
                    rz_order = client.order.create({
                        'amount':   amount_paise,
                        'currency': 'INR',
                        'receipt':  order.order_number,
                        'notes': {
                            'order_number': order.order_number,
                            'customer':     order.name,
                            'phone':        order.phone,
                        }
                    })
                    # Save payment record
                    Payment.objects.create(
                        order=order,
                        razorpay_order_id=rz_order['id'],
                        amount=order.total,
                    )
                    # Go to payment page
                    return render(request, 'cafe/payment.html', {
                        'order':          order,
                        'rz_order_id':    rz_order['id'],
                        'rz_key_id':      cafe_settings.razorpay_key_id,
                        'amount_paise':   amount_paise,
                        'cafe_settings':  cafe_settings,
                    })
                except Exception as e:
                    # Razorpay error — fallback to COD
                    order.payment_method = 'cod'
                    order.status = 'confirmed'
                    order.save()

        # COD / Card / fallback
        request.session['last_order'] = order.order_number
        return redirect('order_confirmation', order_number=order.order_number)

    else:
        messages.error(request, "Please fill in all required delivery details.")
        return render(request, 'cafe/delivery.html', {
            'category_data': build_category_data(),
            'form': form,
            'cart_json': cart_json,
            'cafe_settings': cafe_settings,
        })


@csrf_exempt
def payment_verify(request):
    """
    Razorpay calls this after payment.
    Verify signature → mark order confirmed → show receipt.
    """
    if request.method != 'POST':
        return redirect('delivery_home')

    data = request.POST
    razorpay_order_id   = data.get('razorpay_order_id', '')
    razorpay_payment_id = data.get('razorpay_payment_id', '')
    razorpay_signature  = data.get('razorpay_signature', '')

    try:
        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
        order   = payment.order
        cafe_settings = CafeSettings.get_settings()
        client  = get_razorpay_client()

        if client:
            # Verify signature
            params = {
                'razorpay_order_id':   razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature':  razorpay_signature,
            }
            client.utility.verify_payment_signature(params)

            # Payment verified ✅
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature  = razorpay_signature
            payment.status              = 'success'
            payment.paid_at             = datetime.now()
            payment.save()

            order.status         = 'confirmed'
            order.payment_method = 'upi'
            order.save()

            return redirect('order_confirmation', order_number=order.order_number)

    except Payment.DoesNotExist:
        pass
    except razorpay.errors.SignatureVerificationError:
        # Payment failed / tampered
        try:
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            payment.status = 'failed'
            payment.save()
            payment.order.status = 'pending'
            payment.order.save()
        except Exception:
            pass
        messages.error(request, "Payment verification failed. Please try again or choose Cash on Delivery.")
        return redirect('delivery_home')
    except Exception:
        pass

    messages.error(request, "Something went wrong with payment. Please contact us.")
    return redirect('delivery_home')


@csrf_exempt
def payment_failed(request):
    """User cancelled or payment failed on Razorpay page"""
    order_number = request.GET.get('order', '')
    if order_number:
        try:
            order = DeliveryOrder.objects.get(order_number=order_number)
            order.status = 'pending'
            order.save()
            try:
                order.payment.status = 'failed'
                order.payment.save()
            except Exception:
                pass
        except DeliveryOrder.DoesNotExist:
            pass
    messages.error(request, "Payment was cancelled or failed. You can retry or choose Cash on Delivery.")
    return redirect('delivery_home')


def order_confirmation(request, order_number):
    order        = get_object_or_404(DeliveryOrder, order_number=order_number)
    order_items  = order.items.select_related('menu_item').all()
    cafe_settings = CafeSettings.get_settings()
    payment_info = None
    try:
        payment_info = order.payment
    except Exception:
        pass
    return render(request, 'cafe/order_confirmation.html', {
        'order':         order,
        'order_items':   order_items,
        'cafe_settings': cafe_settings,
        'payment_info':  payment_info,
    })


def receipt_download(request, order_number):
    """Generate printable HTML receipt"""
    order       = get_object_or_404(DeliveryOrder, order_number=order_number)
    order_items = order.items.select_related('menu_item').all()
    cafe_settings = CafeSettings.get_settings()
    return render(request, 'cafe/receipt.html', {
        'order':         order,
        'order_items':   order_items,
        'cafe_settings': cafe_settings,
        'print_mode':    True,
    })


def track_order(request):
    order        = None
    order_items  = []
    order_number = request.GET.get('order_number', '').strip().upper()
    if order_number:
        try:
            order       = DeliveryOrder.objects.get(order_number=order_number)
            order_items = order.items.select_related('menu_item').all()
        except DeliveryOrder.DoesNotExist:
            messages.error(request, f"No order found with #{order_number}.")
    return render(request, 'cafe/track_order.html', {
        'order':        order,
        'order_items':  order_items,
        'order_number': order_number,
    })


def check_delivery_area(request):
    pincode = request.GET.get('pincode', '').strip()
    try:
        area = DeliveryArea.objects.get(pincode=pincode, is_available=True)
        return JsonResponse({'available': True, 'area': area.area_name,
                             'charge': str(area.delivery_charge), 'min_order': str(area.min_order)})
    except DeliveryArea.DoesNotExist:
        return JsonResponse({'available': True, 'area': 'Beed', 'charge': '30', 'min_order': '100'})
