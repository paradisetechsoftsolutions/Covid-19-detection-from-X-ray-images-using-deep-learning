from django.urls import path
from . import views

# urls are routed here based on logic written on the specific views.
urlpatterns = [
	path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('yolo_app', views.yolo_detection_App, name='yolo_app'),
    path('user_history', views.user_details, name='User_History'),
    path('logout', views.logout_user, name ='User_Logout')
]

