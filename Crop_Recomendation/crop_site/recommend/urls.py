from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name = 'home-view'),
    path('signup/', views.signup, name = 'signup-view'),
    path('predict/',views.prediction, name = 'predict-view'),
    path('logout/',views.logout_page, name = 'logout-view'),
    path('login/',views.login_page, name = 'login-view'),
]
