from accounts.views import signup, login_user, signout, profile
from django.urls import path

app_name = "accounts"

urlpatterns = [
    path('profile/', profile, name="profile"),
    path('signup/', signup, name="signup"),
    path('signout', signout, name="signout"),
    path('login', login_user, name="login"),
]
