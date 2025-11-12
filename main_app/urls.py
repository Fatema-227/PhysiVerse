from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='users-profile'),
    path('labs/',views.labs_list,name='labs_list'),
    path('labs/<int:lab_id>/',views.lab_detail,name='lab_detail'),
    path('experiments/<int:exp_id>/',views.experiment_detail,name='experiment_detail'),
    path('accounts/signup/', views.signup, name='signup'),
]
