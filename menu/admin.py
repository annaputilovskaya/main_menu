from django.contrib import admin

from menu.models import Menu, MenuItem


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ["pk", "name"]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ["pk", "menu", "name", "named_url", "parent"]
    list_display_links = ["name"]
    list_filter = ["menu"]
