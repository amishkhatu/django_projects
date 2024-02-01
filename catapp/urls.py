from django.contrib import admin
from django.urls import path, include
from catapp import views

urlpatterns = [
    path('',views.indx ,name='home'),
    path('login',views.loginUser ,name='login'),
    path('logout',views.logoutuser ,name='logout'),
    path('upload',views.upload_file ,name='upload'),
    path('query_builder/',views.query_builder ,name='query_builder'),
    path('add_user/', views.add_user, name='add_user'),
    path('user_list/', views.user_list, name='user_list'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    
]

