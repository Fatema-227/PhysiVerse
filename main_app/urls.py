from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('about/', views.about, name='about'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/',views.edit_profile,name='edit-profile'),
    path('labs/',views.labs_list,name='labs_list'),
    path('labs/<int:lab_id>/',views.lab_detail,name='lab_detail'),
    path('experiments/<int:exp_id>/',views.experiment_detail,name='experiment_detail'),
    path('experiment/<int:exp_id>/discussion/', views.experiment_discussion, name='experiment_discussion'),
    path('accounts/signup/', views.signup, name='signup'),
]
