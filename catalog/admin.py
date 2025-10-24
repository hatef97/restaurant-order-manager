from django.contrib import admin

from .models import Category, Item, Variant, ModifierGroup, ModifierOption


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 1


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "base_price", "is_active", "updated_at")
    list_filter = ("is_active", "category")
    search_fields = ("name", "slug", "sku")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [VariantInline]
    filter_horizontal = ("modifier_groups",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent", "position", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class ModifierOptionInline(admin.TabularInline):
    model = ModifierOption
    extra = 1


@admin.register(ModifierGroup)
class ModifierGroupAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "required",
        "min_choices",
        "max_choices",
        "is_active",
        "position",
    )
    list_filter = ("is_active", "required")
    search_fields = ("name",)
    inlines = [ModifierOptionInline]


@admin.register(ModifierOption)
class ModifierOptionAdmin(admin.ModelAdmin):
    list_display = ("id", "group", "name", "price_delta", "is_active", "position")
    list_filter = ("is_active", "group")
    search_fields = ("name", "group__name")
