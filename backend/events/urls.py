from django.urls import path
from .views import UserSignup, UserLogin, UserLogout, UserIsAuthenticated, get_csrf_token

urlpatterns = [
    path("csrf/", get_csrf_token), 
    path("user/signup/", UserSignup.as_view(), name="signup"),
    path("user/login/", UserLogin.as_view(), name="login"),
    path("user/logout/", UserLogout.as_view(), name="logout"),
    path("user/is-authenticated/", UserIsAuthenticated.as_view(), name="is-authenticated"),
]
