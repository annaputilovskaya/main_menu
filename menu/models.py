from django.db import models

NULLABLE = {"blank": True, "null": True}


class Menu(models.Model):
    """
    Модель меню.
    """

    name = models.CharField(max_length=100, verbose_name="Название меню")

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """
    Модель пункта меню.
    """

    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name="items", verbose_name="Меню"
    )
    name = models.CharField(max_length=100, verbose_name="Название пункта меню")
    named_url = models.SlugField(verbose_name="URL", **NULLABLE)
    parent = models.ForeignKey(
        "self",
        **NULLABLE,
        on_delete=models.CASCADE,
        verbose_name="Пункт вышестоящего уровня",
        related_name="subitems",
    )

    class Meta:
        verbose_name = "Пункт меню"
        verbose_name_plural = "Пункты меню"
        ordering = ["menu", "-parent__id", "name"]

    def __str__(self):
        return f"{self.menu.name} - {self.name}"
