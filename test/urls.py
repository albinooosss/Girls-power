from django.urls import path
from . import views
urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('test/new/', views.test_new, name='test_new'),
]