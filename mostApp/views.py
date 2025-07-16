from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from mostApp.forms import *
from mostApp.models import Post, Profile, ApplicationPost, Certification, Bookmark


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

                auth.login(request, auth.authenticate(email=email, password=password))

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
        user = auth.authenticate(email=email, password=password)
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
    posts = Post.objects.all()
    application_posts = ApplicationPost.objects.all()
    all_posts = posts.union(application_posts).order_by('-created')
    return render(request, 'index.html',  context={'posts': all_posts})

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
    post = ApplicationPost.objects.filter(id=post_id).first()
    return render(request, 'post.html', context={'post': post})

#@login_required(login_url='signin')
def apply(request, post_id):
    if request.method == 'POST':
        form = ApplicationFormModelForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.app_post = ApplicationPost.objects.filter(id=post_id).first()
            form.save()
        return redirect('index')
    form = ApplicationFormModelForm()
    return render(request, 'apply.html', context={'form': form, 'post_id': post_id})

#@login_required(login_url='signin')
def profile(request, username):
    pass

#@login_required(login_url='signin')
def my_profile(request):
    pass

#@login_required(login_url='signin')
def edit_profile(request):
    if request.method == 'POST':
        user = UserEditModelForm(request.POST, request.FILES, instance=request.user)
        profile = ProfileEditModelForm(request.POST, request.FILES, instance=Profile.objects.filter(user=request.user).first())
        if user.is_valid() or profile.is_valid():
            user.save()
            profile.save()
        return redirect('my_profile')
    user = UserEditModelForm(instance=request.user)
    profile = ProfileEditModelForm(instance=Profile.objects.get(user=request.user))
    return render(request, 'edit-profile.html', context={'user': user, 'profile': profile})

#@login_required(login_url='signin')
def bookmark(request):
    pass

#@login_required(login_url='signin')
def collaborations(request):
    pass