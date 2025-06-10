from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .views import DeleteAccountView
from .views import UserProfileView
from django.views.generic import TemplateView
from .views import Model3DViewSet
from rest_framework.routers import DefaultRouter
from .views import Model3DDownloadView
from .views import AtticSkeletonViewSet

from . import views
from . import views
from .views import (
    DeleteAccountView,
    UserProfileView,
    Model3DViewSet,
)

router = DefaultRouter()
router.register(r'models', Model3DViewSet, basename='model3d')
router.register(r'attic-skeletons', AtticSkeletonViewSet)

urlpatterns = [
    path('', views.hello),
    path('api/', views.api),
    path('api/constructions/', views.construction_list),
    path('api/signup/', views.signup_view),
    path('api/login/', views.login_view, name='custom_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', views.logout_view),
    path('api/verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    path('api/delete-account/', DeleteAccountView.as_view(), name='delete-account'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    path('reset-password/', views.reset_password_page, name='reset_password_page'),
    path('api/password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/reset-password-success/', TemplateView.as_view(template_name='main/reset_password_success.html'), name='reset_password_success'),

    path('api/', include(router.urls)),
    path('api/models/<int:pk>/download/', Model3DDownloadView.as_view(), name='model3d-download'),
] + router.urls

urlpatterns += router.urls