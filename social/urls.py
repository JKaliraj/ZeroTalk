from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('register/',views.register,name="register"),
    path('login/',views.login_user,name="login"),
    path('logout/',views.logout_user,name="logout"),
    path('profile_list/',views.profile_list,name="profile_list"),
    path('profile/<int:pk>',views.profile,name="profile"),
    path('update_user/',views.update_user,name="update_user"),
    path('likes/<int:pk>',views.likes,name="likes"),
    path('share/<int:pk>',views.share,name="share"),
]