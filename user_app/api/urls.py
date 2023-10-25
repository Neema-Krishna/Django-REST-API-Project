from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views import RegistrationView,LogOutView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('logout/',LogOutView.as_view(), name='logout'),
    
    # JWT Token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # for login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]