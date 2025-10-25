from rest_framework import serializers

from .models import Category, Item, Variant, ModifierGroup, ModifierOption



class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ["id", "name", "sku", "price_delta", "is_active"]



class ItemSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Item
        fields = [
            "id", "name", "slug", "description", "sku",
            "base_price", "tax_rate", "is_active", "attributes",
            "category", "category_name", "variants",
        ]



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent", "position", "is_active"]



class ModifierOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModifierOption
        fields = ["id", "name", "price_delta", "is_active", "position"]



class ModifierGroupSerializer(serializers.ModelSerializer):
    options = ModifierOptionSerializer(many=True, read_only=True)

    class Meta:
        model = ModifierGroup
        fields = ["id", "name", "required", "min_choices", "max_choices", "is_active", "position", "options"]
