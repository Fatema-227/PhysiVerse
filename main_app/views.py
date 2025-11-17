from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomSignupForm, UpdateProfileForm, TypeForm,AudioNoteForm
from .models import Profile, Lab, Experiment, Comment, Discussion, Reply,AudioNote


def home(request):
    return render(request, 'main_app/home.html')


def about(request):
    return render(request, 'main_app/about.html')


@login_required
def profile_view(request):
    profile = request.user.profile
    user_experiments = Experiment.objects.filter(user=request.user)
    return render(request, 'main_app/profile.html', {'profile': profile ,'user_experiments': user_experiments})


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully ")
            return redirect('profile')
    else:
        form = UpdateProfileForm(instance=profile)

    return render(request, 'main_app/profile_edit.html', {
        'form': form,
        'profile': profile
    })


@login_required
def labs_list(request):
    labs = Lab.objects.all()
    return render(request, 'main_app/labs_list.html', {'labs': labs})


@login_required
def lab_detail(request, lab_id):
    lab = Lab.objects.get(id=lab_id)
    experiments = Experiment.objects.filter(lab=lab)
    return render(request, 'main_app/lab_detail.html', {
        'lab': lab,
        'experiments': experiments
    })


@login_required
def create_experiment(request, lab_id):
    lab = Lab.objects.get(id=lab_id)
    if request.method == 'POST':
        form = TypeForm(request.POST, request.FILES)
        if form.is_valid():
            new_experiment = form.save(commit=False)
            new_experiment.lab = lab
            new_experiment.user = request.user

            if 'video' in request.FILES:
                new_experiment.video = request.FILES['video']

            new_experiment.save()
            messages.success(request, "Experiment created successfully")
            return redirect('lab_detail', lab_id=lab_id)
    else:
        form = TypeForm()

    return render(request, 'main_app/experiment_form.html', {
        'form': form,
        'lab': lab,
        'action': 'Create'
    })


@login_required
def edit_experiment(request, exp_id):
    experiment = Experiment.objects.get(id=exp_id)

    if request.user != experiment.user:
        messages.error(request, "You are not allowed to edit this experiment ")
        return redirect('experiment_detail', exp_id=exp_id)

    if request.method == 'POST':
        form = TypeForm(request.POST, request.FILES, instance=experiment)
        if form.is_valid():
            updated_experiment = form.save(commit=False)

            if 'video' in request.FILES:
                updated_experiment.video = request.FILES['video']

            updated_experiment.save()
            messages.success(request, "Experiment updated successfully ")
            return redirect('experiment_detail', exp_id=exp_id)
    else:
        form = TypeForm(instance=experiment)

    return render(request, 'main_app/experiment_form.html', {
        'form': form,
        'experiment': experiment,
        'action': 'Edit'
    })


@login_required
def delete_experiment(request, exp_id):
    experiment = Experiment.objects.get(id=exp_id)
    lab_id = experiment.lab.id

    if request.user == experiment.user:
        experiment.delete()
        messages.info(request, "Experiment deleted ")

    return redirect('lab_detail', lab_id=lab_id)


@login_required
def experiment_detail(request, exp_id):
    experiment = Experiment.objects.get(id=exp_id)
    comments = Comment.objects.filter(experiment=experiment)
    user_commented = comments.filter(user=request.user).exists()

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(experiment=experiment, user=request.user, content=content)
            messages.success(request, "Your comment has been added ")
            return redirect('experiment_detail', exp_id=exp_id)

    return render(request, 'main_app/experiment_detail.html', {
        'experiment': experiment,
        'comments': comments,
        'user_commented': user_commented
    })


@login_required
def edit_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user == comment.user and request.method == 'POST':
        comment.content = request.POST.get('content')
        comment.save()
        messages.success(request, "Comment updated ")
    return redirect('experiment_detail', exp_id=comment.experiment.id)


@login_required
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    exp_id = comment.experiment.id
    if request.user == comment.user:
        comment.delete()
        messages.info(request, "Comment deleted")
    return redirect('experiment_detail', exp_id=exp_id)


@login_required
def experiment_discussion(request, exp_id):
    experiment = Experiment.objects.get(id=exp_id)
    discussions = Discussion.objects.filter(experiment=experiment).order_by("created_at")

    if request.method == "POST":
        body = request.POST.get("body")
        image = request.FILES.get("image")
        parent_id = request.POST.get("discussion_id")

        if body:
            if parent_id:
                parent_disc = Discussion.objects.get(id=parent_id)
                Reply.objects.create(discussion=parent_disc, user=request.user, body=body, image=image)
            else:
                Discussion.objects.create(experiment=experiment, user=request.user, body=body, image=image)

        return redirect("experiment_discussion", exp_id=exp_id)

    all_replies = Reply.objects.filter(discussion__experiment=experiment).order_by("created_at")

    return render(request, "main_app/discussion.html", {
        "experiment": experiment,
        "discussions": discussions,
        "all_replies": all_replies,
    })


@login_required
def edit_discussion(request, discussion_id):
    discussion = Discussion.objects.get(id=discussion_id)
    if request.user == discussion.user and request.method == 'POST':
        discussion.body = request.POST.get('body')
        if request.FILES.get('image'):
            discussion.image = request.FILES.get('image')
        discussion.save()

    return redirect('experiment_discussion', exp_id=discussion.experiment.id)


@login_required
def delete_discussion(request, discussion_id):
    discussion = Discussion.objects.get(id=discussion_id)
    exp_id = discussion.experiment.id

    if request.user == discussion.user:
        discussion.delete()

    return redirect('experiment_discussion', exp_id=exp_id)


@login_required
def edit_reply(request, reply_id):
    reply = Reply.objects.get(id=reply_id)
    if request.user == reply.user and request.method == 'POST':
        reply.body = request.POST.get('body')
        if request.FILES.get('image'):
            reply.image = request.FILES.get('image')
        reply.save()

    return redirect('experiment_discussion', exp_id=reply.discussion.experiment.id)


@login_required
def delete_reply(request, reply_id):
    reply = Reply.objects.get(id=reply_id)
    exp_id = reply.discussion.experiment.id

    if request.user == reply.user:
        reply.delete()

    return redirect('experiment_discussion', exp_id=exp_id)


@login_required
def add_audio_note(request, exp_id):
    experiment = Experiment.objects.get(id=exp_id)

    if request.method == 'POST':
        form = AudioNoteForm(request.POST, request.FILES)
        if form.is_valid():
            audio_note = form.save(commit=False)
            audio_note.experiment = experiment
            audio_note.user = request.user
            audio_note.save()
            return redirect('experiment_detail', exp_id=exp_id)
    else:
        form = AudioNoteForm()

    return render(request, 'main_app/experiment_detail.html', {
        'experiment': experiment,
        'audio_note_form': form,
    })

@login_required
def edit_audio_note(request, audio_note_id):
    audio_note = AudioNote.objects.get(id=audio_note_id)

    if request.user != audio_note.user:
        return redirect('experiment_detail', exp_id=audio_note.experiment.id)

    if request.method == 'POST':
        form = AudioNoteForm(request.POST, instance=audio_note)
        if form.is_valid():
            form.save()
            return redirect('experiment_detail', exp_id=audio_note.experiment.id)
    else:
        form = AudioNoteForm(instance=audio_note)

    return render(request, 'main_app/edit_audio_note.html', {
        'form': form,
        'audio_note': audio_note,
    })

@login_required
def delete_audio_note(request, audio_note_id):
    audio_note = AudioNote.objects.get(id=audio_note_id)
    exp_id = audio_note.experiment.id

    if request.user == audio_note.user:
        audio_note.delete()

    return redirect('experiment_detail', exp_id=exp_id)


def signup(request):
    error_message = ''

    if request.method == 'POST':
        form = CustomSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            avatar = form.cleaned_data.get('avatar')
            bio = form.cleaned_data.get('bio')

            Profile.objects.create(user=user, avatar=avatar, bio=bio)

            login(request, user)
            messages.success(request, "Your account has been created successfully ")
            return redirect('home')
        else:
            error_message = 'Invalid Sign Up - Try again later...'

    form = CustomSignupForm()
    return render(request, 'registration/signup.html', {
        'form': form,
        'error_message': error_message
    })
