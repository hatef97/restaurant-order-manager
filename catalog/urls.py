from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    ItemViewSet,
    VariantViewSet,
    ModifierGroupViewSet,
    ModifierOptionViewSet,
)


router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"items", ItemViewSet, basename="item")
router.register(r"variants", VariantViewSet, basename="variant")
router.register(r"modifier-groups", ModifierGroupViewSet, basename="modifiergroup")
router.register(r"modifier-options", ModifierOptionViewSet, basename="modifieroption")

urlpatterns = [path("", include(router.urls))]
