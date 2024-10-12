from django.db import models
from django.urls import reverse

from django.db import models
from django.urls import reverse

class Category(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)  

    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('categorie_detail', args=[str(self.id)])


class Product(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    categorie = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='produits')
    image = models.ImageField(upload_to='produits/images/', blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['-date_ajout']
    
    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])
