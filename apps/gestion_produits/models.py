from django.db import models
from django.urls import reverse

from django.db import models
from django.urls import reverse
from django.conf import settings
import joblib
from django.core.exceptions import ValidationError  # Add this import

def charger_filtre():
    return joblib.load(settings.BASE_DIR / 'model_filtre.pkl')
def charger_vectorizer():
    return joblib.load(settings.BASE_DIR / 'tfidf_vectorizer.pkl')
def est_a_archiver(produit):
    vectorizer = charger_vectorizer()
    filtre_modele = charger_filtre()

    produit_nom = produit.nom  
    
    produit_tfidf = vectorizer.transform([produit_nom])  

    label = filtre_modele.predict(produit_tfidf)
    print(produit.nom)
    print(label)
    if label[0] == 0:
        return True  # Signal that this product should be archived
    return False


class Category(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='categories/')  

    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('categorie_detail', args=[str(self.id)])

    def clean(self):
        if not self.nom:
            raise ValidationError({'nom': ""})
        if not self.description:
            raise ValidationError({'description': ""})
        if not self.image:
            raise ValidationError({'image': ""})

class Product(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    categorie = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='produits')
    image = models.ImageField(upload_to='produits/images/')
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
    
    def clean(self):

        if not self.nom:
            raise ValidationError({'nom': ""})
        if not self.description:
            raise ValidationError({'description': ""})
        if not self.prix:
            raise ValidationError({'prix': ""})
        if not self.image:
            raise ValidationError({'image': ""})
        if not self.prix:
            raise ValidationError({'stock': ""})
        # Validation pour le stock
        if self.stock < 0:
            raise ValidationError({'stock': "Le stock ne peut pas être négatif."})
        if self.prix <= 0:
            raise ValidationError({'prix': "Le prix doit être supérieur à zéro."})

    def archiver(self):
        ArchivedProduct.objects.create(
            nom=self.nom,
            description=self.description,
            prix=self.prix,
            stock=self.stock,
            categorie=self.categorie,
            image=self.image,
       
        )
        self.delete()

class ArchivedProduct(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    categorie = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='archived_products') 
    image = models.ImageField(upload_to='produits/images/', blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)