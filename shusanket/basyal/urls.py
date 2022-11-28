from django.urls import path
from .views import UserRegistrationView, UserLoginView, Blog, UserResetPasswordEmail, UserPasswordReset 

urlpatterns = [
path("register/", UserRegistrationView.as_view()),
path("login/", UserLoginView.as_view()),
path("info/", Blog.as_view()),

path("resetpassword/", UserResetPasswordEmail.as_view()),
path("resetp/<uid>/<token>", UserPasswordReset.as_view()),
]
