from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_pk>/profile/', views.user_profile),
    path('<int:user_pk>/follow/', views.follow),    
    path('profile/', views.my_profile),
    path('<int:user_pk>/update/', views.update_profile),
    path('<int:user_pk>/delete/', views.delete_account),  

]
