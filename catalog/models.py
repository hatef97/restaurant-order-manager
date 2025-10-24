from django.db import models
from django.contrib.postgres.fields import JSONField


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    position = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["position", "name"]
        indexes = [models.Index(fields=["slug"]), models.Index(fields=["is_active"])]

    def __str__(self):
        return self.name


class Item(TimeStampedModel):
    category = models.ForeignKey(
        Category, null=True, blank=True, related_name="items", on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=64, unique=True, null=True, blank=True)
    base_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0)  # e.g. 9.00 = 9%
    is_active = models.BooleanField(default=True)
    attributes = models.JSONField(default=dict, blank=True)

    modifier_groups = models.ManyToManyField("ModifierGroup", blank=True, related_name="items")

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["slug"]), models.Index(fields=["is_active"])]

    def __str__(self):
        return self.name


class Variant(TimeStampedModel):
    item = models.ForeignKey(Item, related_name="variants", on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    sku = models.CharField(max_length=64, unique=True, null=True, blank=True)
    price_delta = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [("item", "name")]
        indexes = [models.Index(fields=["is_active"])]

    def __str__(self):
        return f"{self.item.name} — {self.name}"


class ModifierGroup(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    required = models.BooleanField(default=False)
    min_choices = models.PositiveIntegerField(default=0)
    max_choices = models.PositiveIntegerField(default=1)  # 1 = radio, >1 = multi
    is_active = models.BooleanField(default=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position", "name"]

    def __str__(self):
        return self.name


class ModifierOption(TimeStampedModel):
    group = models.ForeignKey(ModifierGroup, related_name="options", on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    price_delta = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = [("group", "name")]
        ordering = ["group", "position", "name"]
        indexes = [models.Index(fields=["is_active"])]

    def __str__(self):
        return f"{self.group.name} — {self.name}"
