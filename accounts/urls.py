from .views import SignUpView, VerifyCodeApiView, GetNewCodeVerify, ChangeInfoUserApi, TokenRefreshApi, CreatePhotoUserApi, LoginApi, LogOutApi, ForgotPasswordApi, ResetPasswordApi, UpdatePasswordApi
from django.urls import path

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('verify/', VerifyCodeApiView.as_view()),
    path('new-verify/', GetNewCodeVerify.as_view()),
    path('change-info/', ChangeInfoUserApi.as_view()),
    path("token-refresh/", TokenRefreshApi.as_view()),
    path('create-photo/', CreatePhotoUserApi.as_view()),
    path('login/', LoginApi.as_view()),
    path('logout/', LogOutApi.as_view()),
    path('forgot-pass/', ForgotPasswordApi .as_view()),
    path('reset-pass/', ResetPasswordApi.as_view()),
    path('update-pass/', UpdatePasswordApi.as_view()),

]