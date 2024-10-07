from django import template

from menu.models import MenuItem
from menu.services import get_subitems, get_uri

register = template.Library()


@register.inclusion_tag("menu/main_menu.html", takes_context=True)
def draw_menu(context, menu_name: str) -> dict:
    """
    Рисует меню с учетом вложенности пунктов меню.
    Активный пункт меню определяется по URL текущей страницы.
    Все, что над выделенным пунктом - развернуто.
    Первый уровень вложенности под выделенным пунктом тоже развернут.
    """

    # Получаем текущий адрес
    request_uri = str(context["request"].path)

    # Получаем все пункты меню с заданным именем меню из БД
    menu_items = list(MenuItem.objects.filter(menu__name=menu_name))
    menu_items.sort(key=lambda x: x.name)

    # Формируем список пунктов меню первого уровня и
    # определяем активный пункт меню.
    all_items = []
    active_item = None
    nested_items = []
    result_items = []
    for i in menu_items:
        item_value = {
            "id": i.id,
            "name": i.name,
            "uri": get_uri(i),
            "subitems": [],
            "parent": i.parent,
            "is_expanded": False,
            "is_active": False,
        }
        all_items.append(item_value)

    for item in all_items:
        if request_uri == item["uri"]:
            item["is_active"] = True
            item["is_expanded"] = True
            active_item = item
            active_root = item
            while active_root["parent"]:
                active_root = active_root["parent"]
                active_root = list(
                    filter(lambda x: x["id"] == active_root.id, all_items)
                )[0]
                active_root["is_expanded"] = True
        if item["parent"]:
            nested_items.append(item)
        else:
            result_items.append(item)

    if active_item is None:
        return {"items": result_items, "menu": menu_name}

    # Разворачиваем все подпункты меню выше активного пункта
    # и подпукты первого уровня активного пункта меню
    get_subitems(result_items, nested_items)

    return {"items": result_items, "menu": menu_name}
