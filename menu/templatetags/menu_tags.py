from django import template

from menu.models import MenuItem
from menu.services import get_upper_subitems, get_uri

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
    active_item = None
    nested_items = []
    result_items = []
    for item in menu_items:
        item_value = {
            "id": item.id,
            "name": item.name,
            "uri": get_uri(item),
            "subitems": [],
            "parent": item.parent,
        }

        if request_uri == item_value["uri"]:
            active_item = item_value
            active_root = item
            while active_root.parent:
                active_root = active_root.parent
        if not item_value["parent"]:
            result_items.append(item_value)
        else:
            nested_items.append(item_value)

    if active_item is None:
        return {"items": result_items, "menu": menu_name}

    # Находим индекс корня активного элемента
    active_root_item = [
        item for item in result_items if item.get("id") == active_root.pk
    ][0]
    index = result_items.index(active_root_item)
    print(index)

    # Разворачиваем пункты меню выше корня активного элемента
    if index > 0:
        for i in range(index):
            result_items[i]["subitems"] = list(
                filter(lambda x: x["parent"].id == result_items[i]["id"], nested_items)
            )
            if result_items[i]["subitems"]:
                get_upper_subitems(result_items[i]["subitems"], nested_items)

    # # Разворачиваем пункты меню в корне активного элемента до активного элемента
    # # и подпункты  активного элемента первого уровня вложенности
    # if active_root_item["id"] != active_item["id"]:
    #     active_root_item["subitems"] = list(
    #         filter(lambda x: x["parent"].id == active_root_item["id"], nested_items)
    #     )
    #     if active_root_item["subitems"]:
    #         get_subitems(active_root_item["subitems"], nested_items, active_item)
    # else:
    #     active_root_item["subitems"] = list(
    #         filter(lambda x: x["parent"].id == active_root_item["id"], nested_items)
    #     )

    return {"items": result_items, "menu": menu_name}
