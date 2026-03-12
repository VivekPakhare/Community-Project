from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('draft', 'Draft'),
        ('removed', 'Removed'),
    ]

    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
    ]

    BILL_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    # Core fields
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='good')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Brand & Specifications
    brand = models.CharField(max_length=100, blank=True, help_text='e.g. Apple, Samsung, Dell, Nike')
    ram = models.CharField(max_length=50, blank=True, help_text='e.g. 8 GB')
    processor = models.CharField(max_length=100, blank=True, help_text='e.g. Intel i5 12th Gen')
    storage = models.CharField(max_length=50, blank=True, help_text='e.g. 256 GB SSD')
    battery_health = models.CharField(max_length=50, blank=True, help_text='e.g. 87%')
    author = models.CharField(max_length=200, blank=True, help_text='Book author')
    edition = models.CharField(max_length=100, blank=True, help_text='Book edition')

    # Location
    location = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=200, blank=True)
    pin_code = models.CharField(max_length=10, blank=True)

    # Seller Contact
    seller_name = models.CharField(max_length=200, blank=True, help_text='Contact name')
    seller_phone = models.CharField(max_length=15, blank=True, help_text='Contact phone number')

    # Chat Availability
    chat_enabled = models.BooleanField(default=True, help_text='Allow buyers to chat')
    call_enabled = models.BooleanField(default=False, help_text='Allow buyers to call')

    # Optional Fields
    reason_for_selling = models.CharField(max_length=300, blank=True)
    purchase_year = models.PositiveIntegerField(null=True, blank=True)
    warranty_available = models.BooleanField(default=False)
    bill_available = models.CharField(max_length=3, choices=BILL_CHOICES, default='no')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.title}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['product', 'buyer']
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.buyer.username} - {self.rating}/5"
