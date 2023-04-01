from django.conf.urls.static import static
from django.urls import path

from stackoverflowClone1 import settings
from users.views import CustomLoginView, CustomLogoutView, UserSignUpView, user_page, edit_profile

app_name = 'users'

urlpatterns = [
    path('sign-in/', CustomLoginView.as_view(), name='sign-in'),
    path('sign-out/', CustomLogoutView.as_view(), name='sign-out'),
    path('sign-up/', UserSignUpView.as_view(), name='sign-up'),
    path('profile/', user_page, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
