from web_project.template_helpers.theme import TemplateHelper

class TemplateLayout:
    def init(self, context):
        user = context.get('user')  
        layout = "user"  

        if user is not None:
            if user.is_superuser:
                layout = "vertical"  
            elif user.is_authenticated:
                
                if user.role == 'VENDEUR':
                    layout = "vertical"  
                elif user.role == 'CLIENT':
                    layout = "user"  
                else:
                    layout = "user"  
        context.update(
            {
                "layout_path": TemplateHelper.set_layout(
                    "layout_" + layout + ".html", context
                ),
            }
        )

        TemplateHelper.map_context(context)

        return context
