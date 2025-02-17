from django.urls import path
from .views import UserSignup, UserLogin, UserLogout, EditProfile, GetProfile, CreateEvent, EditEvent, DeleteEvent

urlpatterns = [
    # Endpoints User
    path("user/signup/", UserSignup.as_view(), name="signup"),
    path("user/login/", UserLogin.as_view(), name="login"),
    path("user/logout/", UserLogout.as_view(), name="logout"),
    path("user/profile/edit/", EditProfile.as_view(), name="edit-profile"),
    path("user/profile/", GetProfile.as_view(), name="get-profile"),
    path("event/create/", CreateEvent.as_view(), name="create-event"),
    path("event/edit/", EditEvent.as_view(), name="edit-event"),
    path("event/delete/", DeleteEvent.as_view(), name="delete-event"),
]
