from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Lab,Experiment,Comment

# Create your views here.
def home(request):
    return render(request,'main_app/home.html')

def about(request):
    return render(request,'main_app/about.html')

def labs_list(request):
    labs=Lab.objects.all()
    return render(request,'labs_list.html', {'labs':labs})

def signup(request):
    error_message=''
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('index')
        else:
            error_message='Invalid Sign Up -Try again later...'

    form=UserCreationForm()
    context={'form':form ,'error_message':error_message}
    return render(request,'registration/signup.html',context)
