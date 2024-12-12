from __future__ import annotations

from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView

from .views import PostViewSet
from .views import UserViewSet


class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "jwt_tokens"


class ThrottledTokenRefreshView(TokenRefreshView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "jwt_tokens"


class ThrottledTokenVerifyView(TokenVerifyView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "jwt_tokens"


router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"posts", PostViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path(
        "api/token/", ThrottledTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", ThrottledTokenRefreshView.as_view(), name="token_refresh"
    ),
    path("api/token/verify/", ThrottledTokenVerifyView.as_view(), name="token_verify"),
]

# GET /posts/by-author/<author_id>/
