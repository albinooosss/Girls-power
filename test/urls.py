from django.urls import path
from . import views
urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('test/new/', views.create_test(), name='test_new'),
    path('test/<int:pk>/', views.passing_the_test(), name='test_detail'),

]