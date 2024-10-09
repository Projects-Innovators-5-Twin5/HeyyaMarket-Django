from django.shortcuts import render
from django.views.generic import TemplateView
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from .models import Product, Category
from .forms import ProductForm, CategoryForm
class ProductView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user 
        template_layout = TemplateLayout()
        context = template_layout.init(context)

        return context

class CategoryListView(ListView):
    
    model = Category
    template_name = 'categories/categorie_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'categories/categorie_detail.html'
    context_object_name = 'categorie'

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/categorie_form.html'
    success_url = reverse_lazy('categorie_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        layout = "vertical"  

        context.update(
            {
                "layout_path": TemplateHelper.set_layout(
                    "layout_" + layout + ".html", context

                ),
            }
        )
        
        return context

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/categorie_form.html'
    success_url = reverse_lazy('categorie_list')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'produits/categorie_confirm_delete.html'
    success_url = reverse_lazy('categorie_list')


class ProductListView(ListView):
    model = Product
    template_name = 'produits/product_list.html'
    context_object_name = 'produits'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'produits/product_detail.html'
    context_object_name = 'produit'

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'produits/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'produits/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'produits/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')
