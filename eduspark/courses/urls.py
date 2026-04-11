from django.urls import path

from . import views

urlpatterns = [
    path('materials/<int:material_id>/file/', views.material_stream, name='material_stream'),
    path('materials/<int:material_id>/', views.material_viewer, name='material_viewer'),
    path('lecture/<int:video_id>/', views.video_lecture, name='video_lecture'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('', views.course_list, name='course_list'),
]
