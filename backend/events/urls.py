from django.urls import path

from .views import (
    # User-related views
    UserSignup,
    UserLogin,
    UserLogout,
    EditProfile,
    GetProfile,

    # Event-related views
    CreateEvent,
    EditEvent,
    DeleteEvent,
    GetEventView,

    # Attendee-related views
    GetAttendeeList,
    GetPendingInvites,
    GetJoinedEventsList,
    RemoveAttendee,
    JoinEvent,
    LeaveEvent,
    InviteToEvent,
)

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
    path("event/<int:event_id>/", GetEventView.as_view(), name="get-event"),
    path("event/<int:event_id>/attendees/", GetAttendeeList.as_view(), name="event-attendees"),
    path("event/join/", JoinEvent.as_view(), name="join-event"),
    path("event/leave/", LeaveEvent.as_view(), name="leave-event"),
    path("event/invite/", InviteToEvent.as_view(), name="invite-to-event"),
    path("event/<int:event_id>/pending_invites/", GetPendingInvites.as_view(), name="pending-invites"),
    path("event/remove_attendee/", RemoveAttendee.as_view(), name="remove-attendee"),
    path("user/events/joined/", GetJoinedEventsList.as_view(), name="joined-events"),
]

