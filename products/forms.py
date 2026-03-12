from django import forms
from .models import Product, ProductImage
import datetime


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title', 'description', 'price', 'category', 'condition',
            # Brand & Specs
            'brand', 'ram', 'processor', 'storage', 'battery_health', 'author', 'edition',
            # Location
            'location', 'city', 'area', 'pin_code',
            # Seller Contact
            'seller_name', 'seller_phone',
            # Chat Availability
            'chat_enabled', 'call_enabled',
            # Optional
            'reason_for_selling', 'purchase_year', 'warranty_available', 'bill_available',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your product in detail...'}),
            'price': forms.NumberInput(attrs={'min': '1', 'step': '0.01', 'placeholder': '₹ Price'}),
            'brand': forms.TextInput(attrs={'placeholder': 'e.g. Apple, Samsung, Dell'}),
            'ram': forms.TextInput(attrs={'placeholder': 'e.g. 8 GB'}),
            'processor': forms.TextInput(attrs={'placeholder': 'e.g. Intel i5 12th Gen'}),
            'storage': forms.TextInput(attrs={'placeholder': 'e.g. 256 GB SSD'}),
            'battery_health': forms.TextInput(attrs={'placeholder': 'e.g. 87%'}),
            'author': forms.TextInput(attrs={'placeholder': 'e.g. R.S. Aggarwal'}),
            'edition': forms.TextInput(attrs={'placeholder': 'e.g. 5th Edition'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Near Main Gate'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'area': forms.TextInput(attrs={'placeholder': 'Area / Locality'}),
            'pin_code': forms.TextInput(attrs={'placeholder': 'Pin Code'}),
            'seller_name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'seller_phone': forms.TextInput(attrs={'placeholder': '10-digit phone number'}),
            'reason_for_selling': forms.TextInput(attrs={'placeholder': 'e.g. Upgrading to new model'}),
            'purchase_year': forms.NumberInput(attrs={'min': '2000', 'max': datetime.date.today().year, 'placeholder': 'e.g. 2024'}),
        }

    def clean_pin_code(self):
        pin = self.cleaned_data.get('pin_code', '').strip()
        if pin and (not pin.isdigit() or len(pin) != 6):
            raise forms.ValidationError('Enter a valid 6-digit pin code.')
        return pin

    def clean_seller_phone(self):
        phone = self.cleaned_data.get('seller_phone', '').strip()
        if phone and (not phone.isdigit() or len(phone) != 10):
            raise forms.ValidationError('Enter a valid 10-digit phone number.')
        return phone


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image', 'is_primary']
