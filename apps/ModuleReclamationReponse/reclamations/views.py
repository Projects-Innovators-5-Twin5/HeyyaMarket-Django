from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView
from .models import Reclamation, Reponse
from .forms import ReclamationForm, ReponseForm
from django.urls import reverse_lazy
from transformers import pipeline
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from transformers import pipeline
from django.http import JsonResponse
from web_project import TemplateLayout
from .utils.dialogflow_utils import detect_intent_texts
# Import correct
from django.shortcuts import render
from web_project.template_helpers.theme import TemplateHelper
from django.http import JsonResponse
from transformers import GPTNeoForCausalLM, GPT2Tokenizer
import openai
import torch

# Initialiser le modèle de génération de texte

# Charger le modèle et le tokenizer
# Charger le modèle et le tokenizer une seule fois au démarrage de l'application
#model = GPTNeoForCausalLM.from_pretrained('EleutherAI/gpt-neo-125M')
#tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
import os
from dotenv import load_dotenv
import cohere

# Charger les variables d'environnement
load_dotenv()
COHERE_API_KEY = os.getenv('COHERE_API_KEY')
if COHERE_API_KEY:
    cohere_client = cohere.Client(COHERE_API_KEY)
else:
    raise ValueError("La clé API Cohere est introuvable. Assurez-vous qu'elle est définie dans le fichier .env.")

# Fonction de génération de texte avec Cohere
def generate_text(prompt):
    try:
        response = cohere_client.generate(
            model='command',  # Remplacer 'xlarge' par un modèle disponible tel que 'command'
            prompt=prompt,
            max_tokens=50,
            temperature=0.6
        )
        return response.generations[0].text.strip()
    except Exception as e:
        # Gestion de l'erreur avec un message approprié
        return f"Une erreur est survenue lors de la génération de texte : {str(e)}"

# Vue Django pour analyser une réclamation
class AnalyzeComplaintView(View):
    def get(self, request, complaint_id):
        try:
            complaint = Reclamation.objects.get(id=complaint_id)
        except Reclamation.DoesNotExist:
            return JsonResponse({"error": "Réclamation non trouvée"}, status=404)

        complaint_text = complaint.description
        generated_response = generate_text(complaint_text)

        # Check if an error occurred during generation
        if "erreur" in generated_response.lower():
            return JsonResponse({"error": generated_response}, status=500)

        return JsonResponse({"response": generated_response})

    def post(self, request, complaint_id):  # Use 'complaint_id' consistently
        # Retrieve the complaint
        complaint = get_object_or_404(Reclamation, id=complaint_id)

        # Generate the automatic response with Cohere
        generated_response = generate_text(complaint.description)

        # Add the generated response to the database
        reponse = Reponse(
            reclamation=complaint,
            texte=generated_response,
            utilisateur=complaint.utilisateur
        )
        reponse.save()

        # Update the complaint status to "resolved"
        complaint.statut = "resolue"
        complaint.save()

        # Prepare the email content
        subject = f"Réponse à votre réclamation #{complaint.id}"
        html_content = render_to_string('reclamations/reponse_email.html', {
            'utilisateur': complaint.utilisateur,
            'reclamation': complaint,
            'reponse': reponse  # Pass the response to the email template
        })
        text_content = strip_tags(html_content)  # Convert HTML to plain text

        # Create the email with text and HTML content
        email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [complaint.utilisateur.email])
        email.attach_alternative(html_content, "text/html")

        # Send the email
        email.send()

        # Success message
        messages.success(request, "La réponse générée a été ajoutée avec succès, et un email a été envoyé à l'utilisateur.")

        # Redirect to the list of complaints
        return redirect('liste_reclamations')


class AjouterReclamationView(CreateView):
    model = Reclamation
    form_class = ReclamationForm
    template_name = 'reclamations/ajouter_reclamation.html'
    success_url = reverse_lazy('ReclamationFront')

    def form_valid(self, form):
        form.instance.utilisateur = self.request.user
        messages.success(self.request, "Réclamation ajoutée avec succès.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Il y a des erreurs dans le formulaire, veuillez les corriger.")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_user.html", context),
            }
        )
        return context



class ListeReclamationsView(ListView):
    model = Reclamation
    template_name = 'reclamations/liste_reclamations.html'
    context_object_name = 'reclamations'
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Update the context
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
            }
        )

        return context


from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from .models import Reclamation
from .forms import ReponseForm

from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib.auth import get_user_model
from .models import Reclamation
from .forms import ReponseForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
User = get_user_model()  # Récupérer le modèle utilisateur



from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Reclamation, Reponse  # Assurez-vous que les modèles sont importés
from .forms import ReponseForm  # Assurez-vous que votre formulaire est importé
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class RepondreReclamationView(View):
    def get(self, request, reclamation_id):
        # Récupérer la réclamation
        reclamation = get_object_or_404(Reclamation, id=reclamation_id)


        # Si la priorité n'est pas basse, afficher le formulaire de réponse manuelle
        form = ReponseForm()
        return render(request, 'reclamations/repondre_reclamation.html', {
            'form': form,
            'reclamation': reclamation
        })

    def post(self, request, reclamation_id):
        # Récupérer la réclamation
        reclamation = get_object_or_404(Reclamation, id=reclamation_id)
        form = ReponseForm(request.POST)

        if form.is_valid():
            # Créer une nouvelle réponse sans la sauvegarder tout de suite
            reponse = form.save(commit=False)
            reponse.reclamation = reclamation

            # Assigner l'utilisateur à partir de la réclamation
            reponse.utilisateur = reclamation.utilisateur
            reponse.save()

            # Mettre à jour le statut de la réclamation en "résolue"
            reclamation.statut = "resolue"
            reclamation.save()

            # Préparer le contenu de l'email
            subject = f"Réponse à votre réclamation #{reclamation.id}"
            html_content = render_to_string('reclamations/reponse_email.html', {
                'utilisateur': reclamation.utilisateur,
                'reclamation': reclamation
            })
            text_content = strip_tags(html_content)  # Convertir le contenu HTML en texte brut

            # Créer l'email avec contenu texte et HTML
            email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [reclamation.utilisateur.email])
            email.attach_alternative(html_content, "text/html")

            # Envoyer l'email
            email.send()

            # Message de succès
            messages.success(request, "Votre réponse a été ajoutée avec succès, et un email a été envoyé à l'utilisateur.")

            # Rediriger vers la liste des réclamations
            return redirect('liste_reclamations')

        # Si le formulaire n'est pas valide, renvoyer le formulaire avec les erreurs
        return render(request, 'reclamations/repondre_reclamation.html', {
            'form': form,
            'reclamation': reclamation
        })

class ModifierReclamationView(View):
    def get_object(self, reclamation_id):
        # Récupérer la réclamation spécifique
        return get_object_or_404(Reclamation, id=reclamation_id)

    def post(self, request, reclamation_id):
        # Récupérer la réclamation
        reclamation = self.get_object(reclamation_id)

        # Mettre à jour les champs de la réclamation avec les données soumises
        reclamation.titre = request.POST.get('titre')
        reclamation.description = request.POST.get('description')

        reclamation.statut = request.POST.get('statut')
        reclamation.save()  # Sauvegarder les modifications

        return redirect('liste_reclamations')  # Rediriger vers la liste après modification

    def get(self, request, reclamation_id):
        # Si l'on veut gérer un GET pour afficher des détails ou rediriger
        return redirect('liste_reclamations')
class SupprimerReclamationView(View):
    def post(self, request, reclamation_id):
        # Récupérer la réclamation à supprimer
        reclamation = get_object_or_404(Reclamation, id=reclamation_id)

        # Supprimer la réclamation
        reclamation.delete()

        # Rediriger vers la liste des réclamations après suppression
        return redirect('liste_reclamations')
class RechercheReclamations(View):
    def get(self, request):
        query = request.GET.get('query', '')
        reclamations = Reclamation.objects.filter(titre__icontains=query)
        results = [{'id': reclamation.id, 'titre': reclamation.titre, 'date_creation': reclamation.date_creation,
                    'priorite': reclamation.priorite, 'statut': reclamation.statut} for reclamation in reclamations]
        return JsonResponse(results, safe=False)
class ListeReclamationsFrontView(ListView):
    model = Reclamation
    template_name = 'reclamations/LIsteReclamation.html'
    context_object_name = 'reclamations'
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Update the context
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_user.html", context),
            }
        )

        return context
def analyze_sentiment(text):
    # Utiliser le pipeline de Hugging Face pour l'analyse de sentiment
    classifier = pipeline("sentiment-analysis")
    result = classifier(text)[0]  # Récupère le premier résultat

    # Extraire le label (sentiment) des résultats
    label = result['label'].lower()

    # Mapper les labels aux résultats attendus
    if label == 'neutral':
        return 'neutre'
    elif label == 'positive':
        return 'positive'
    elif label == 'negative':
        return 'negative'
    else:
        return 'neutre'  # Par défaut neutre si le label n'est pas reconnu

class ComplaintsAnalyzer(View):
    def get(self, request):
        # Extraire les descriptions des réclamations
        descriptions = Reclamation.objects.values_list('description', flat=True)

        # Appeler la fonction analyze_sentiment pour chaque description
        sentiment_results = [analyze_sentiment(description) for description in descriptions]

        # Calculer les pourcentages
        total = len(sentiment_results)
        neutral_count = sum(1 for result in sentiment_results if result == 'neutre')
        positive_count = sum(1 for result in sentiment_results if result == 'positive')
        negative_count = sum(1 for result in sentiment_results if result == 'negative')

        # Calcul des pourcentages
        neutral_percentage = (neutral_count / total) * 100 if total > 0 else 0
        positive_percentage = (positive_count / total) * 100 if total > 0 else 0
        negative_percentage = (negative_count / total) * 100 if total > 0 else 0

        # Renvoyer les résultats
        return JsonResponse({
            'neutral_percentage': neutral_percentage,
            'positive_percentage': positive_percentage,
            'negative_percentage': negative_percentage,
        })
