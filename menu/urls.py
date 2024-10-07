from django.urls import path

from menu.apps import MenuConfig
from menu.views import MainMenuView

app_name = MenuConfig.name

urlpatterns = [
    path("", MainMenuView.as_view(), name="main"),
    path("<slug:slug>", MainMenuView.as_view(), name="slug_item"),
    path("<int:pk>", MainMenuView.as_view(), name="item"),
]
