from django.urls import reverse


def get_uri(item):
    """
    Получает адрес ссылки пункта меню.
    """

    if item.named_url:
        item_uri = reverse("menu:slug_item", args=[item.named_url])
    else:
        item_uri = reverse("menu:item", args=[item.pk])
    return item_uri


def get_upper_subitems(items, nested_items):
    """
    Рекурсивно получает подпункты пунктов меню выше корня активного элемента.
    """
    for item in items:
        item["subitems"] = list(
            filter(lambda x: x["parent"].id == item["id"], nested_items)
        )
        if item["subitems"]:
            get_upper_subitems(item["subitems"], nested_items)


def get_subitems(items, nested_items, active_item):
    """
    Рекурсивно получает подпункты пунктов меню в корне активного элемента до активного элемента
    и подпункты  активного элемента первого уровня вложенности
    """
    pass
