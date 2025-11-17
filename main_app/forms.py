from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Experiment,AudioNote
from django.forms import ModelForm

class CustomSignupForm(UserCreationForm):
    avatar = forms.ImageField(required=True, label='Profile Picture')
    bio = forms.CharField(
        required=True,
        label='Bio',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write something about yourself...'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'avatar', 'bio']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']

class TypeForm(ModelForm):
    class Meta:
        model=Experiment
        fields=['title','description','Simulation_Data','video','procedure']

class AudioNoteForm(forms.ModelForm):
    class Meta:
        model = AudioNote
        fields = ['audio_file', 'note']
