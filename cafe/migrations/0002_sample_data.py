from django.db import migrations


def add_sample_menu_items(apps, schema_editor):
    MenuItem = apps.get_model('cafe', 'MenuItem')

    items = [
        # Ice Cream Sundaes
        {"name": "Classic Vanilla Sundae", "description": "Rich vanilla ice cream topped with hot fudge, whipped cream & cherry.", "price": 120, "category": "ice_cream", "is_bestseller": True},
        {"name": "Brownie Blast Sundae", "description": "Warm brownie pieces layered with chocolate ice cream & caramel drizzle.", "price": 150, "category": "ice_cream", "is_bestseller": False},
        {"name": "Strawberry Delight", "description": "Fresh strawberry ice cream with real strawberry compote & nuts.", "price": 130, "category": "ice_cream", "is_bestseller": False},

        # Milkshakes
        {"name": "Classic Chocolate Shake", "description": "Thick, creamy chocolate milkshake blended to perfection.", "price": 110, "category": "milkshakes", "is_bestseller": True},
        {"name": "Oreo Crunch Shake", "description": "Vanilla shake blended with crushed Oreo cookies & whipped cream.", "price": 130, "category": "milkshakes", "is_bestseller": True},
        {"name": "Strawberry Bliss Shake", "description": "Fresh strawberry milkshake with a creamy, smooth texture.", "price": 120, "category": "milkshakes", "is_bestseller": False},

        # Cold Coffee
        {"name": "Classic Cold Coffee", "description": "Chilled blended coffee with milk & sugar — a Star Queen staple.", "price": 90, "category": "cold_coffee", "is_bestseller": True},
        {"name": "Mocha Cold Coffee", "description": "Rich espresso blended with chocolate syrup and cold milk.", "price": 110, "category": "cold_coffee", "is_bestseller": False},
        {"name": "Cold Coffee Frappe", "description": "Iced coffee frappe topped with whipped cream and coffee dust.", "price": 130, "category": "cold_coffee", "is_bestseller": False},

        # Pizza
        {"name": "Margherita Pizza", "description": "Classic tomato base, mozzarella cheese, fresh basil leaves.", "price": 180, "category": "pizza", "is_bestseller": False},
        {"name": "Veg Supreme Pizza", "description": "Loaded with peppers, onions, mushrooms, olives & sweet corn.", "price": 220, "category": "pizza", "is_bestseller": True},
        {"name": "Paneer Tikka Pizza", "description": "Spiced paneer tikka with capsicum on a tandoori base.", "price": 240, "category": "pizza", "is_bestseller": False},

        # Burgers
        {"name": "Classic Veg Burger", "description": "Crispy veg patty with lettuce, tomato, cheese & special sauce.", "price": 120, "category": "burgers", "is_bestseller": False},
        {"name": "Spicy Aloo Burger", "description": "Masala aloo tikki with pickled onions & mint chutney.", "price": 110, "category": "burgers", "is_bestseller": True},
        {"name": "Cheese Double Burger", "description": "Double patty loaded with cheddar cheese, jalapenos & mayo.", "price": 160, "category": "burgers", "is_bestseller": False},

        # Momos
        {"name": "Steamed Veg Momos", "description": "Soft steamed dumplings stuffed with spiced vegetables. (6 pcs)", "price": 100, "category": "momos", "is_bestseller": True},
        {"name": "Fried Veg Momos", "description": "Crispy fried dumplings with fiery red chutney. (6 pcs)", "price": 120, "category": "momos", "is_bestseller": False},
        {"name": "Paneer Momos", "description": "Soft momos stuffed with spiced cottage cheese. (6 pcs)", "price": 130, "category": "momos", "is_bestseller": False},

        # French Fries
        {"name": "Classic Salted Fries", "description": "Golden crispy fries seasoned with sea salt.", "price": 80, "category": "french_fries", "is_bestseller": False},
        {"name": "Masala Fries", "description": "Crispy fries tossed in our signature masala blend.", "price": 95, "category": "french_fries", "is_bestseller": True},
        {"name": "Loaded Cheese Fries", "description": "Golden fries smothered in melted cheese & herbs.", "price": 120, "category": "french_fries", "is_bestseller": False},

        # Fresh Juices
        {"name": "Fresh Orange Juice", "description": "Freshly squeezed oranges, served chilled.", "price": 80, "category": "fresh_juices", "is_bestseller": False},
        {"name": "Watermelon Juice", "description": "Cool, refreshing watermelon juice — summer in a glass.", "price": 70, "category": "fresh_juices", "is_bestseller": True},
        {"name": "Mix Fruit Juice", "description": "Seasonal fruits blended fresh — nature's best.", "price": 90, "category": "fresh_juices", "is_bestseller": False},

        # Smoothies
        {"name": "Mango Smoothie", "description": "Thick Alphonso mango blended with yogurt & honey.", "price": 130, "category": "smoothies", "is_bestseller": True},
        {"name": "Berry Blast Smoothie", "description": "Mixed berries blended with yogurt & a hint of vanilla.", "price": 140, "category": "smoothies", "is_bestseller": False},

        # Lassi
        {"name": "Sweet Lassi", "description": "Classic chilled sweet yogurt drink — Punjabi style.", "price": 80, "category": "lassi", "is_bestseller": True},
        {"name": "Mango Lassi", "description": "Creamy yogurt blended with ripe Alphonso mango pulp.", "price": 100, "category": "lassi", "is_bestseller": False},
        {"name": "Rose Lassi", "description": "Fragrant rose-flavoured lassi with dry fruits.", "price": 90, "category": "lassi", "is_bestseller": False},

        # Falooda
        {"name": "Classic Rose Falooda", "description": "Chilled rose milk with vermicelli, basil seeds & ice cream.", "price": 130, "category": "falooda", "is_bestseller": True},
        {"name": "Kesar Falooda", "description": "Saffron-infused falooda with pista kulfi & dry fruits.", "price": 160, "category": "falooda", "is_bestseller": True},
        {"name": "Chocolate Falooda", "description": "Rich chocolate falooda with chocolate ice cream on top.", "price": 150, "category": "falooda", "is_bestseller": False},
    ]

    for item in items:
        MenuItem.objects.create(**item, is_available=True)


def remove_sample_menu_items(apps, schema_editor):
    MenuItem = apps.get_model('cafe', 'MenuItem')
    MenuItem.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_sample_menu_items, remove_sample_menu_items),
    ]
