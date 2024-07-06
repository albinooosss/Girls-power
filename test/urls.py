from django.urls import path
from . import views
urlpatterns = [
    path('profile', views.login, name='profile'),
    path('register/', views.register, name='register'),
    path('', views.main_page, name='main_page'),
    path('test/my_tests/', views.my_tests, name='my_tests'),
    path('test/passed_tests', views.passed_tests, name='passed_tests'),
    path('test/passing_the_test/<int:pk>/', views.passing_the_test, name='passing_the_test'),
    path('test/FAQ', views.FAQ, name='FAQ'),
    # path('test/create_test/', views.create_test, name='create_test'),
    # path('test/<int:pk>/edit_test/', views.edit_test, name='edit_test'),
    path('accounts/login/', views.login, name='login'),


]