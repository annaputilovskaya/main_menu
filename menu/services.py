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


def get_subitems(items, nested_items):
    """
    Рекурсивно разворачивает все подпукнты меню до активного элемента
    и подпункты  активного элемента первого уровня вложенности.
    """
    index = next((i for i, item in enumerate(items) if item["is_expanded"] is True), -1)
    if index != -1:
        for i in range(index + 1):
            items[i]["subitems"] = list(
                filter(lambda x: x["parent"].id == items[i]["id"], nested_items)
            )
            if items[i]["is_active"]:
                break
            else:
                if items[i]["subitems"]:
                    get_subitems(items[i]["subitems"], nested_items)
    else:
        for item in items:
            item["subitems"] = list(
                filter(lambda x: x["parent"].id == item["id"], nested_items)
            )
            if item["subitems"]:
                get_subitems(item["subitems"], nested_items)
