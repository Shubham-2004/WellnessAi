# from django.urls import path
# from .import views

# urlpatterns = [
#     path('register/',views.register,name='register'),
#     path('login/',views.login_view,name='login'),
#     path('dashboard/',views.dashboard,name='dashboard'),
#     path('meeting/',views.videocall,name='meeting'),
#     path('logout/',views.logout_view, name='logout'),
#     path('join/',views.join_room, name='join_room'),
#     path('',views.index, name='index'),

    
# ]

from django.contrib import admin
from django.urls import path
from wellnessai import settings
from welnessapp import views
from django.conf.urls.static import static

urlpatterns = [
    
    path('loginn/',views.loginn),
    path('signup/',views.signup),
    path('logoutt/',views.logoutt),
    path('upload',views.upload),
    path('wellnessWizard', views.wellnessWizard, name='wellnessWizard'),
    path('like-post/<str:id>', views.likes, name='like-post'),
    path('#<str:id>', views.home_post),
    path('explore',views.explore),
    path('profile/<str:id_user>', views.profile),
    path('delete/<str:id>', views.delete),
    path('search-results/', views.search_results, name='search_results'),
    path('follow', views.follow, name='follow'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('meeting/',views.videocall,name='meeting'),
    path('logout/',views.logout_view, name='logout'),
    path('join/',views.join_room, name='join_room'),
    path('',views.home),
    
    
]
