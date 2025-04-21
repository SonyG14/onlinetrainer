from django.urls import path, include
from . import views
from .views import UserInfoView
from .views import RegisterView

urlpatterns = [
    path('', views.index,  name='index'),
    path('about-us', views.about,  name='about-us'),
    path('profile', views.profile,  name='profile'),
    path('contacts', views.contacts,  name='contacts'),
    path('registration_form/', views.registration_form, name='registration_form'),
    path('login/', views.login, name='login'),
    path('api/userinfo/', UserInfoView.as_view(), name='user-info'),
    path('api/register/', RegisterView.as_view(), name='register'),

]
