from django.urls import path

from . import views

urlpatterns = [
    path('lecture/<int:video_id>/', views.video_lecture, name='video_lecture'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('', views.course_list, name='course_list'),
]
