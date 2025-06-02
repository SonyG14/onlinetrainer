from django.urls import path, include
from . import views
from .views import UserInfoView
from .views import RegisterView
from .views import ActivateUserView
from .views import RegisterAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomTokenObtainPairView
from .views import try_mobile_login
from .views import upload_raw_data_YUV_frames

urlpatterns = [
    path('', views.index,  name='index'),
    path('about-us', views.about,  name='about-us'),
    path('profile', views.profile_p, name='profile'),
    path('contacts', views.contacts,  name='contacts'),
    path('registration_form/', views.registration_form, name='registration_form'),
    path('login/', views.login, name='login'),
    path('downloads/', views.downloads, name='downloads'),
    path('exit/', views.exit, name='exit'),
    path('exercises/', views.exercises, name='exercises'),
    path('ex1/', views.ex1, name='ex1'),
    path('ex2/', views.ex2, name='ex2'),
    path('ex3/', views.ex3, name='ex3'),
    path('api/userinfo/', UserInfoView.as_view(), name='user-info'),
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateUserView.as_view(), name='activate'),
    path('activation-success/', views.activation_success, name='activation_success'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('chose1/', views.chose1, name='chose1'),
    path('chose2/', views.chose2, name='chose2'),
    path('chose3/', views.chose3, name='chose3'),
    path('mobile_login', try_mobile_login, name='try_mobile_login'),
    path('upload_raw_YUV_frames', upload_raw_data_YUV_frames, name='upload_raw_package_YUV_frames'),




]

