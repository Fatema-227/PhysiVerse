from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomSignupForm
from .forms import UpdateProfileForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Profile,Lab,Experiment,Comment

# Create your views here.
def home(request):
    return render(request,'main_app/home.html')

def about(request):
    return render(request,'main_app/about.html')

@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'main_app/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UpdateProfileForm(instance=profile)

    return render(request, 'main_app/profile_edit.html', {'form': form})

@login_required
def labs_list(request):
    labs=Lab.objects.all()
    return render(request,'main_app/labs_list.html', {'labs':labs})

@login_required
def lab_detail(request,lab_id):
    lab=Lab.objects.get(id=lab_id)
    experiments=Experiment.objects.filter(lab=lab)
    return render(request,'main_app/lab_detail.html',{'lab':lab , 'experiments':experiments})

@login_required
def experiment_detail(request,exp_id):
    experiment=Experiment.objects.get(id=exp_id)
    comments = Comment.objects.filter(experiment=experiment, parent__isnull=True)
    return render(request,'main_app/experiment_detail.html',{'experiment':experiment ,'comments': comments})


def signup(request):
    error_message=''
    if request.method=='POST':
        form=CustomSignupForm(request.POST,request.FILES)
        if form.is_valid():
            user=form.save()
            avatar = form.cleaned_data.get('avatar')
            bio = form.cleaned_data.get('bio')
            Profile.objects.create(user=user,avatar=avatar, bio=bio)
            login(request,user)
            return redirect('home')
        else:
            error_message='Invalid Sign Up -Try again later...'

    form=CustomSignupForm()
    context={'form':form ,'error_message':error_message}
    return render(request,'registration/signup.html',context)
