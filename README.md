# Student Marketplace SaaS

A SaaS platform where students can buy and sell products within their campus community.

## Features

- **User Management** – Registration, login, profile management, college verification
- **Product Marketplace** – Create/edit/delete listings with images, categories, and conditions
- **Search & Discovery** – Keyword search, category/price/condition/location filters
- **Order System** – Place orders, seller confirms, buyer marks completed
- **Messaging** – Real-time chat between buyer and seller per product
- **Admin Dashboard** – Manage users, products, reports, and view analytics
- **REST API** – Full API endpoints via Django REST Framework
- **Monetization Ready** – Listing fees, featured listings, seller subscriptions

## Tech Stack

- **Backend**: Python, Django, Django REST Framework
- **Frontend**: Django Templates, Bootstrap 5, Bootstrap Icons
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Deployment**: Docker, Gunicorn

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Visit http://127.0.0.1:8000/

## Docker

```bash
docker-compose up --build
```

## Default Admin Credentials

- **Username**: admin
- **Password**: admin123

## Project Structure

```
├── accounts/          # User management (registration, login, profiles)
├── products/          # Product listings, categories, reviews
├── orders/            # Order system and payments
├── messaging/         # Chat conversations and reports
├── admin_dashboard/   # Admin management interface
├── templates/         # HTML templates (Bootstrap 5)
├── static/            # Static assets
├── media/             # User-uploaded files
├── student_marketplace/  # Project settings and root URLs
├── manage.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/accounts/api/register/` | Register new user |
| GET/PUT | `/accounts/api/profile/` | Get/update profile |
| GET/POST | `/products/api/` | List/create products |
| GET/PUT/DELETE | `/products/api/<id>/` | Product detail |
| GET | `/products/api/categories/` | List categories |
| GET/POST | `/orders/api/` | List/create orders |
| GET/PUT | `/orders/api/<id>/` | Order detail |
| GET | `/messages/api/` | List conversations |
| GET/POST | `/messages/api/<id>/messages/` | Conversation messages |

## Key URLs

- `/` – Home page
- `/products/` – Browse products
- `/products/create/` – List a product
- `/orders/` – My orders
- `/messages/` – My conversations
- `/dashboard/` – Admin dashboard
- `/admin/` – Django admin
