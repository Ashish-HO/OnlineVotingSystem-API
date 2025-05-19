from django.urls import path, include
from . import views

urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/<int:pk>/", views.UserViewDetail.as_view()),
    path("candidates/", views.CandidateView.as_view()),
    path("candidates/<int:pk>/", views.CandidateDetail.as_view()),
    path("posts", views.PostView.as_view()),
    path("posts/<int:pk>/", views.PostDetailView.as_view()),
    path("voter", views.VoterView.as_view()),
    path("ballot", views.BallotView.as_view()),
    path("login/", views.LoginView.as_view(), name="login"),
]
