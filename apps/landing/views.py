from django.shortcuts import render

from django.views.generic import TemplateView
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper

class LandingView(TemplateView):
    template_name = 'your_template.html'  # Specify your actual template

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
