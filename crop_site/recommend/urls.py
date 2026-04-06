from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name = 'home-view'),
    path('signup/', views.signup, name = 'signup-view'),
    path('predict/',views.predicting, name = 'predict-view'),
    path('logout/',views.logout_page, name = 'logout-view'),
    path('login/',views.login_page, name = 'login-view'),
    path('history/',views.history, name = 'history-view'),
    path('delete_entry/<int:id>/',views.delete_user_entry, name = 'delete_entry-view'),
    path('profile/',views.profile, name = 'profile-view'),
    path('change_password/',views.change_password, name = 'password-view'),
    path('admin_dashboard/',views.admin_dashboard, name = 'admin-dashboard-view'),
    path('admin_login/',views.admin_login, name = 'admin-login-view'),
    path('admin_logout/',views.admin_logout, name = 'admin-logout-view'),
    path('admin_users/',views.admin_users, name = 'admin-users-view'),
    path('delete_user/<int:id>/',views.delete_user, name = 'delete-user-view'),
    path('admin_pred/',views.admin_prediction, name = 'admin-prediction-view'),
    path('admin_delete_pred/<int:id>/',views.admin_delete_pred, name = 'admin-delete-prediction-view'),
]
