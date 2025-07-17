from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from mostApp.forms import *
from mostApp.models import *


# Create your views here.

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password == password_confirm:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email is Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=email, email=email, password=password)
                user.save()

                auth.login(request, auth.authenticate(username=email, password=password))

                user_model = User.objects.filter(email=email).first()
                new_profile = Profile.objects.create(user=user_model, first_name=first_name, last_name=last_name)
                new_profile.save()
                return redirect('/')
        else:
            messages.info(request, 'Passwords Not Matching')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

#@login_required(login_url='signin')
def index(request):
    posts = Post.objects.all().order_by('-created')
    profiles = Profile.objects.all()
    return render(request, 'index.html',  context={'posts': posts,  'profiles': profiles})

#@login_required(login_url='signin')
def browse(request):
    posts = ApplicationPost.objects.all()
    return render(request, 'browse.html', context={'posts': posts})

#@login_required(login_url='signin')
def create_post(request):
    if request.method == 'POST':
        form = ApplicationPostModelForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.profile = Profile.objects.filter(user=request.user).first()
            post.save()
        return redirect('index')

    form = ApplicationPostModelForm()
    return render(request, 'create.html', context={'form': form})

#@login_required(login_url='signin')
def post(request, post_id):
    exists  = False
    post = ApplicationPost.objects.filter(id=post_id).first()
    if ApplicationForm.objects.filter(user=request.user,  app_post_id=post_id).exists():
        exists = True
    return render(request, 'post.html', context={'post': post, 'exists': exists})

#@login_required(login_url='signin')
def apply(request, post_id):
    apply =  True # if the user tries to apply to their own post
    profile = Profile.objects.filter(user=request.user).first()
    if ApplicationPost.objects.filter(id=post_id).first().profile == profile:
        apply = False
    if request.method == 'POST':
        form = ApplicationFormModelForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.app_post = ApplicationPost.objects.filter(id=post_id).first()
            form.user = request.user
            form.save()
        return redirect('index')
    form = ApplicationFormModelForm()
    return render(request, 'apply.html', context={'form': form, 'post_id': post_id, 'apply': apply})

#@login_required(login_url='signin')
def profile(request, user_id):
    edit = False
    user = User.objects.filter(id=user_id).first()
    if request.user == user:  # currently signed-in user
        profile = Profile.objects.filter(user=request.user).first()
        edit = True
    else:
        profile = Profile.objects.filter(user=user).first()
    posts = Post.objects.filter(profile=profile)
    application_posts = ApplicationPost.objects.filter(profile=profile)
    all_posts = posts.union(application_posts).order_by('-created')
    certifications = Certification.objects.filter(profile=profile).order_by('-date')
    return render(request, 'profile.html', context={'profile': profile, 'posts': all_posts, 'certifications': certifications, 'edit': edit})

#@login_required(login_url='signin')
def edit_profile(request):
    if request.method == 'POST':
        user = UserEditModelForm(request.POST, request.FILES, instance=request.user)
        profile = ProfileEditModelForm(request.POST, request.FILES, instance=Profile.objects.filter(user=request.user).first())
        if user.is_valid() or profile.is_valid():
            user.save()
            profile.save()
        return redirect('profile', request.user.pk)
    user = UserEditModelForm(instance=request.user)
    profile = ProfileEditModelForm(instance=Profile.objects.get(user=request.user))
    return render(request, 'edit-profile.html', context={'user': user, 'profile': profile})

#@login_required(login_url='signin')
def bookmark_post(request, post_id):
    profile = Profile.objects.filter(user=request.user).first()
    post = Post.objects.filter(id=post_id).first()
    if BookmarkPost.objects.filter(profile=profile, post=post).exists():
        BookmarkPost.objects.filter(profile=profile, post=post).delete()
    else:
        BookmarkPost.objects.create(profile=profile, post=post).save()
    return redirect(index)

#@login_required(login_url='signin')
def bookmark_app_post(request, post_id):
    profile = Profile.objects.filter(user=request.user).first()
    post = ApplicationPost.objects.filter(id=post_id).first()
    if BookmarkAppPost.objects.filter(profile=profile, post=post).exists():
        BookmarkAppPost.objects.filter(profile=profile, post=post).delete()
    else:
        BookmarkAppPost.objects.create(profile=profile, post=post).save()
    return redirect(index)

#@login_required(login_url='signin')
def bookmarks(request):
    bookmarks_post = BookmarkPost.objects.filter(profile=Profile.objects.filter(user=request.user).first())
    bookmarks_app_post = BookmarkAppPost.objects.filter(profile=Profile.objects.filter(user=request.user).first())
    return render(request, 'bookmarks.html', context={'bookmarks_post': bookmarks_post, 'bookmarks_app_post': bookmarks_app_post})

#@login_required(login_url='signin')
def collaborations(request, user_id):
    user = User.objects.filter(id=user_id).first()
    collaborations_sent = Collaboration.objects.filter(user=user)
    collaborations_received = Collaboration.objects.filter(collaborator=Profile.objects.filter(user=user).first())
    return render(request, 'collaborations.html', {'collaborations_sent': collaborations_sent, 'collaborations_received': collaborations_received})

def collaborate(request, user_id):
    subject = request.POST['subject']
    body = request.POST['body']
    collaboration = Collaboration.objects.filter(user=request.user, collaborator=Profile.objects.filter(user_id=user_id).first())
    if collaboration.exists():
        collaboration.update(subject=subject, body=body)
    else:
        Collaboration.objects.create(user=request.user, collaborator=Profile.objects.filter(user_id=user_id).first(), subject=subject, body=body)
    return redirect(profile, user_id)

def applied(request):
    posts = ApplicationForm.objects.filter(user=request.user)
    return render(request, 'applied.html', context={'posts': posts})