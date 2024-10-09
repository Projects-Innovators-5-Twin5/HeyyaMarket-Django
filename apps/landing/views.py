from django.shortcuts import render

from django.views.generic import TemplateView
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper

class LandingView(TemplateView):
    template_name = 'your_template.html'  # Specify your actual template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user 
        template_layout = TemplateLayout()
        context = template_layout.init(context)

        return context
