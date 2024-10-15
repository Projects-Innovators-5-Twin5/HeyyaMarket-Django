from django.shortcuts import render, get_object_or_404 
from django.views.generic import TemplateView
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView,View
)
from django.urls import reverse_lazy
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from django.shortcuts import redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator, Page

class CategoryView(ListView):
    model = Category
    template_name = 'categories/categories.html'
    context_object_name = 'categories'
    paginate_by = 5  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = TemplateLayout.init(self, context)
        context['form'] = CategoryForm()
        categories_list = Category.objects.all()
        paginator = Paginator(categories_list, 5)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['categories'] = page_obj

        return context

    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Catégorie ajoutée avec succés.'}) 
        else:
            context = self.get_context_data()
            context['form'] = form
            return JsonResponse({'success': False, 'message': 'Erreur lors de lajout de la catégorie.'})

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
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context



class CategoryUpdateView(View):
    def get(self, request, pk):
            categorie = get_object_or_404(Category, pk=pk) 
            form = CategoryForm(instance=categorie)

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                rendered_form = render_to_string('categories/update_categorie_form.html', {'form': form}, request=request)
                return JsonResponse({
                    'form': rendered_form 
                })
            else:
                return render(request, 'categories/update_categorie_form.html', {'form': form})

    def post(self, request, pk):
        categorie = get_object_or_404(Category, pk=pk)
        form = CategoryForm(request.POST, request.FILES, instance=categorie)

        if form.is_valid():
            form.save()  
            return JsonResponse({'success': True, 'message': 'Catégorie mise à jour avec succès!'}) 
        else:
            return JsonResponse({'error': False, 'message': 'Erreur lors de la mise à jour de la catégorie.'})


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'produits/categorie_confirm_delete.html'
    success_url = reverse_lazy('categorie_list')

    def post(self, request, *args, **kwargs):
        category = self.get_object()  # Get the category instance to delete
        category.delete()  # Delete the category

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Catégorie supprimée avec succès!'})
        return super().post(request, *args, **kwargs)


class ProductView(ListView):
    model = Product
    template_name = 'produits/produits.html'
    context_object_name = 'produits'
    paginate_by = 5  
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        produits_list = Product.objects.all()
        paginator = Paginator(produits_list, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['form'] = ProductForm()
        context['produits'] = page_obj
        return context

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Produit ajoutée avec succés.'}) 
        else:
            context = self.get_context_data()
            context['form'] = form
            return JsonResponse({'success': False, 'message': 'Erreur lors dajout de produit.'}) 


class ProductDetailView(DetailView):
    model = Product
    template_name = 'produits/front/details_produit.html'
    context_object_name = 'produit'
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_user.html", context),
                "container_class": ""
            }
        )

        return context

class ProductDetailBackView(DetailView):
    model = Product
    template_name = 'produits/details_produit.html'
    context_object_name = 'produit'
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        

        return context

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'produits/product_form.html'
    success_url = reverse_lazy('product_list')

class ProductUpdateView(View):
    def get(self, request, pk):
            produit = get_object_or_404(Product, pk=pk) 
            form = ProductForm(instance=produit)

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                rendered_form = render_to_string('produits/update_produit_form.html', {'form': form}, request=request)
                return JsonResponse({
                    'form': rendered_form 
                })
            else:
                return render(request, 'produits/update_produit_form.html', {'form': form})

    def post(self, request, pk):
        produit = get_object_or_404(Product, pk=pk)
        form = ProductForm(request.POST, request.FILES, instance=produit)

        if form.is_valid():
            form.save()  
            return JsonResponse({'success': True, 'message': 'Produit mis à jour avec succès!'}) 
        else:
            return JsonResponse({'error': False, 'message': 'Erreur lors de la mise à jour du produit.'})

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'produits/categorie_confirm_delete.html'
    def post(self, request, *args, **kwargs):

        produit = self.get_object() 
        produit.delete() 

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Produit supprimé avec succès!'})
        return super().post(request, *args, **kwargs)

class ProductFrontView(ListView):
    model = Product
    template_name = 'produits/front/produits.html'
    context_object_name = 'produits'
    paginate_by = 8  

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        
        produits_list = Product.objects.all()
        
        paginator = Paginator(produits_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        categories = Category.objects.all()[:4]  
        context['form'] = ProductForm()
        context['produits'] = page_obj
        context['categories'] = categories  
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_user.html", context),
                "container_class": ""
            }
        )

        return context

class ProductLandingView(ListView):
    model = Product
    template_name = 'produits/front/produits.html'
    context_object_name = 'produits'
    paginate_by = 7  

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        
        produits_list = Product.objects.all()
        
        paginator = Paginator(produits_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        categories = Category.objects.all()[:4]  
        context['form'] = ProductForm()
        context['produits'] = page_obj
        context['categories'] = categories  
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_user.html", context),
                "container_class": ""
            }
        )

        return context        