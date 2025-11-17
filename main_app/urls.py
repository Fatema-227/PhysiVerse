from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit-profile"),
    path("labs/", views.labs_list, name="labs_list"),
    path("labs/<int:lab_id>/", views.lab_detail, name="lab_detail"),
    path("lab/<int:lab_id>/create-experiment/", views.create_experiment, name="create_experiment"),
    path("experiment/<int:exp_id>/edit/", views.edit_experiment, name="edit_experiment"),
    path("experiment/<int:exp_id>/delete/", views.delete_experiment, name="delete_experiment"),
    path("experiments/<int:exp_id>/", views.experiment_detail, name="experiment_detail"),
    path("experiment/<int:exp_id>/discussion/", views.experiment_discussion, name="experiment_discussion"),
    path("discussion/edit/<int:discussion_id>/", views.edit_discussion, name="edit_discussion"),
    path("discussion/delete/<int:discussion_id>/", views.delete_discussion, name="delete_discussion"),
    path("reply/edit/<int:reply_id>/", views.edit_reply, name="edit_reply"),
    path("reply/delete/<int:reply_id>/", views.delete_reply, name="delete_reply"),
    path("comment/edit/<int:comment_id>/", views.edit_comment, name="edit_comment"),
    path("comment/delete/<int:comment_id>/", views.delete_comment, name="delete_comment"),
    path("experiment/<int:exp_id>/add-audio-note/", views.add_audio_note, name="add_audio_note"),
    path("audio-note/edit/<int:audio_note_id>/", views.edit_audio_note, name="edit_audio_note"),
    path("audio-note/delete/<int:audio_note_id>/", views.delete_audio_note, name="delete_audio_note"),
    path("accounts/signup/", views.signup, name="signup"),
]
