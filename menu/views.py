from django.views.generic import TemplateView


class MainMenuView(TemplateView):
    """
    Контроллер для отображения главного меню сайта.
    """

    template_name = "menu/base.html"
