from django.urls import path
from . import views
urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('test/create_test/', views.create_test, name='create_test'),
    path('test/passing_the_test/<int:pk>/', views.passing_the_test, name='passing_the_test'),
    path('test/<int:pk>/edit_test/', views.edit_test, name='edit_test'),
    path('test/my_tests', views.my_tests, name='my tests'),
    path('test/passed_tests', views.passed_tests, name='passed tests'),
    path('test/FAQ', views.FAQ, name='FAQ'),


]