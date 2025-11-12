from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('about/', views.about, name='about'),
    path('labs/',views.labs_list,name='labs_list'),
    path('accounts/signup/', views.signup, name='signup'),
]
