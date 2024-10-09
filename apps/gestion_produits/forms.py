from django import forms
from .models import Product, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['nom', 'description']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['nom', 'description', 'prix', 'stock', 'categorie', 'image']