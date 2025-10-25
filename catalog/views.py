from rest_framework import viewsets, mixins, filters

from .models import Category, Item, Variant, ModifierGroup, ModifierOption
from .serializers import (
    CategorySerializer,
    ItemSerializer,
    VariantSerializer,
    ModifierGroupSerializer,
    ModifierOptionSerializer,
)


class ReadOnlyViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    pass


class CategoryViewSet(ReadOnlyViewSet):
    queryset = Category.objects.filter(is_active=True).order_by("position", "name")
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "slug"]


class ItemViewSet(ReadOnlyViewSet):
    queryset = (
        Item.objects.filter(is_active=True)
        .select_related("category")
        .prefetch_related("variants", "modifier_groups")
        .order_by("name")
    )
    serializer_class = ItemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "slug", "sku"]

    def get_queryset(self):
        qs = super().get_queryset()
        cat = self.request.query_params.get("category")
        if cat:
            qs = qs.filter(category_id=cat)
        return qs


class VariantViewSet(ReadOnlyViewSet):
    queryset = (
        Variant.objects.filter(is_active=True).select_related("item").order_by("item__name", "name")
    )
    serializer_class = VariantSerializer


class ModifierGroupViewSet(ReadOnlyViewSet):
    queryset = ModifierGroup.objects.filter(is_active=True).order_by("position", "name")
    serializer_class = ModifierGroupSerializer


class ModifierOptionViewSet(ReadOnlyViewSet):
    queryset = (
        ModifierOption.objects.filter(is_active=True)
        .select_related("group")
        .order_by("group__name", "position")
    )
    serializer_class = ModifierOptionSerializer
