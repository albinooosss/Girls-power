from django.urls import path
from . import views
urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('test/create_test/', views.create_test, name='create_test'),
    path('test/passing_the_test/<int:pk>/', views.passing_the_test, name='passing_the_test'),
    path('test/<int:pk>/edit_test/', views.edit_test, name='edit_test'),

]