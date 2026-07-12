from django.urls import path 

from user.View.user_view import (
    UserSignUpView,
    UserLoginView,
    UserLogoutView
)


urlpatterns = [
path('signup/', UserSignUpView.as_view(), name='user-signup'),
path('login/', UserLoginView.as_view(), name='user-login'), 
path('logout/', UserLogoutView.as_view(), name='user-logout'),

]