from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomSignupForm
from .forms import UpdateProfileForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Profile,Lab,Experiment,Comment,Discussion,Reply

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

    return render(request, 'main_app/profile_edit.html', {'form': form, 'profile':profile})

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
    comments = Comment.objects.filter(experiment=experiment)
    user_commented = comments.filter(user=request.user).exists()

    if request.method=='POST' and request.user.is_authenticated:
        content=request.POST.get('content')

        if content:
            Comment.objects.create(experiment=experiment,user=request.user, content=content)
            return redirect('experiment_detail',exp_id=exp_id)

    return render(request,'main_app/experiment_detail.html',{'experiment':experiment ,'comments': comments , 'user_commented': user_commented})


@login_required
def experiment_discussion(request, exp_id):
    experiment = Experiment.objects.get(id=exp_id)

    discussions = Discussion.objects.filter(experiment=experiment).order_by("created_at")

    if request.method == "POST":
        body = request.POST.get("body")
        image = request.FILES.get("image")
        parent_discussion_id = request.POST.get("discussion_id")

        if body:
            if parent_discussion_id:
                discussion = Discussion.objects.get(id=parent_discussion_id)
                Reply.objects.create(discussion=discussion,user=request.user,body=body,image=image)
            else:
                Discussion.objects.create(experiment=experiment,user=request.user,body=body,image=image)
        return redirect("experiment_discussion", exp_id=exp_id)

    all_replies = Reply.objects.filter(discussion__experiment=experiment).order_by("created_at")

    return render(request, "main_app/discussion.html", {"experiment": experiment,"discussions": discussions,"all_replies": all_replies,})


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
