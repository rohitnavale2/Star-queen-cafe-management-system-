# ⭐ Star Queen Cafe — Django Web Application

**The Family Cafe & Bistro | Beed, Maharashtra, India**

---

## 📁 Project Structure

```
starqueen/
├── manage.py
├── requirements.txt
├── db.sqlite3              ← auto-created after migrate
├── starqueen/              ← Django project config
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── cafe/                   ← Main Django app
    ├── __init__.py
    ├── admin.py            ← Admin registrations
    ├── forms.py            ← Reservation form
    ├── models.py           ← MenuItem, Reservation, GalleryImage
    ├── urls.py             ← App URL routes
    ├── views.py            ← View functions (MVT)
    ├── migrations/
    │   ├── 0001_initial.py
    │   └── 0002_sample_data.py   ← 30+ sample menu items
    ├── templates/cafe/
    │   ├── base.html       ← Navbar + Footer layout
    │   ├── home.html       ← Hero + Bestsellers + Categories
    │   ├── menu.html       ← Full menu with category filter
    │   ├── gallery.html    ← Image gallery with hover zoom
    │   ├── events.html     ← Events cards
    │   ├── visit.html      ← Address + Google Maps embed
    │   └── reservation.html← Booking form
    └── static/cafe/
        ├── css/style.css   ← Luxury black & gold theme
        └── js/script.js    ← Scroll, particles, animations
```

---

## 🚀 Installation & Setup

### Step 1 — Clone / Extract the project
```bash
cd starqueen/
```

### Step 2 — Create a virtual environment (recommended)
```bash
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on Mac/Linux:
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Run database migrations
```bash
python manage.py migrate
```
This creates `db.sqlite3` and populates **30+ sample menu items** automatically.

### Step 5 — Create an admin superuser
```bash
python manage.py createsuperuser
```
Follow the prompts to set a username, email, and password.

### Step 6 — Run the development server
```bash
python manage.py runserver
```

### Step 7 — Open in browser
| URL | Page |
|-----|------|
| http://127.0.0.1:8000/ | Home |
| http://127.0.0.1:8000/menu/ | Menu |
| http://127.0.0.1:8000/gallery/ | Gallery |
| http://127.0.0.1:8000/events/ | Events |
| http://127.0.0.1:8000/visit/ | Visit Us |
| http://127.0.0.1:8000/reservation/ | Reserve a Table |
| http://127.0.0.1:8000/admin/ | Django Admin Panel |

---

## 🎨 Design Theme

- **Background:** Deep Black `#0a0a0a`
- **Accent:** Luxury Gold `#c9a84c`
- **Typography:** Playfair Display (headings) + Montserrat (body)
- **Style:** Luxury cafe — elegant, responsive, dark mode

---

## 📋 Models

### `MenuItem`
| Field | Type | Notes |
|-------|------|-------|
| name | CharField | Item name |
| description | TextField | Optional description |
| price | DecimalField | In Indian Rupees (₹) |
| category | CharField | 11 categories (choices) |
| is_available | BooleanField | Toggle visibility |
| is_bestseller | BooleanField | Featured on home page |

### `Reservation`
| Field | Type | Notes |
|-------|------|-------|
| name | CharField | Guest name |
| phone | CharField | Contact number |
| date | DateField | Booking date |
| time | TimeField | Booking time |
| guests | PositiveIntegerField | 1–20 guests |
| special_request | TextField | Optional |
| status | CharField | pending / confirmed / cancelled |

### `GalleryImage`
| Field | Type | Notes |
|-------|------|-------|
| title | CharField | Image label |
| category | CharField | interior / food / customers |
| image_url | URLField | Direct image URL |

---

## ⚙️ Admin Panel

Log in at `/admin/` to:
- **Add/edit menu items** — set prices, categories, bestseller flag
- **Manage reservations** — view bookings, update status (pending → confirmed)
- **Add gallery images** — paste image URLs for interior/food/customer photos

---

## 📞 Contact Details to Update

Replace these placeholders in the code with your actual info:
- `+91 XXXXX XXXXX` — phone number (in `base.html`, `visit.html`, `reservation.html`)
- `hello@starqueencafe.com` — email (in `visit.html`)
- Instagram/Facebook/WhatsApp links (in `base.html`, `visit.html`)
- Google Maps embed URL (in `visit.html`) — replace with your exact location

---

## ✅ Quick Commands Reference

```bash
python manage.py migrate          # Apply migrations
python manage.py runserver        # Start dev server
python manage.py createsuperuser  # Create admin user
python manage.py collectstatic    # Collect static files (production)
```

---

*Built with Django MVT Architecture · Bootstrap 5 · SQLite · Luxury Black & Gold Design*
