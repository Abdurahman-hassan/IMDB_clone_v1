from rest_framework.authtoken.views import obtain_auth_token

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import Register, Logout, RegisterWithJWT

urlpatterns = [
    path('login/', obtain_auth_token, name='obtain-token'),
    path('register/', Register.as_view(), name='register'),
    path('register-with-jwt/', RegisterWithJWT.as_view(), name='register-with-jwt'),
    path('logout/', Logout.as_view(), name='logout'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # we can't revoke the access token, and we need to wait for the token to expire
    # only i can remove user or remove token from db
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
