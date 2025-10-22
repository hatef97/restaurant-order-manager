from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



def health(_): return JsonResponse({"status": "ok"})



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    u = request.user
    return JsonResponse({"id": u.id, "email": u.email, "first_name": u.first_name, "last_name": u.last_name})

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/me/", me),
]
