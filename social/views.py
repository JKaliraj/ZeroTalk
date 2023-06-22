from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile,Talk
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import TalkForm,RegisterForm,UpdateUserForm,ProfileImageForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm


def home(req):
    if req.user.is_authenticated:
        form = TalkForm(req.POST or None)
        if req.method == 'POST':
            if form.is_valid():
                talks = form.save(commit=False)
                talks.user = req.user
                talks.save()
                messages.success(req,"You Tweet Posted Successfuly")
                return redirect('home')
        talks = Talk.objects.all().order_by("-created")
        return render(req,"home.html",{"talks":talks,"form":form})
    else:
        talks = Talk.objects.all().order_by("-created")
        return render(req,"home.html",{"talks":talks})

def profile_list(req):
    if req.user.is_authenticated:
        profiles = Profile.objects.exclude(user = req.user)
        return render(req,"profile_list.html",{"profiles":profiles})
    else:
        messages.success(req,"You must be logged in to view this page!")
        return redirect('home')
    
def profile(req,pk):
    if req.user.is_authenticated:
        profile = Profile.objects.get(user_id = pk)
        talks = Talk.objects.filter(user_id = pk).order_by("-created")

        if req.method == 'POST':
            current_user_profile = req.user.profile
            action = req.POST['follow']
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
            current_user_profile.save()
        if profile.user==req.user:
            showBtn = False
        else:
            showBtn = True
        return render(req,"profile.html",{"profile":profile,"talks":talks,"showBtn":showBtn})
    else:
        messages.success(req,"You must be logged in to view this page!")
        return redirect('home')
    


def login_user(req):
    if req.method=='POST':
        username = req.POST['username']
        password = req.POST['password']
        user = authenticate(req,username=username,password=password )
        if user is not None:
            login(req,user)
            messages.success(req,"You Successfully logged in😎!")
            return redirect('home')
        else:
            messages.success(req,"Wrong Credentials...Try again!")
            return redirect('login')


    else:
        return render(req,"login.html",{})
    


def logout_user(req):
    logout(req)
    messages.success(req,"You Have Been logged out😴!")
    return redirect('home')

def register(req):
    form = RegisterForm()
    if req.method=='POST':
        form = RegisterForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # firstname = form.cleaned_data['firstname']
            # lastname = form.cleaned_data['lastname']
            # email = form.cleaned_data['email']
            user = authenticate(username=username,password=password)
            login(req,user)
            messages.success(req,"You Successfully Registered 😎!")
            return redirect('home')
    return render(req,"register.html",{"form":form})


def update_user(req):
    if req.user.is_authenticated:
        curr_user = User.objects.get(id=req.user.id)
        profile_user = Profile.objects.get(user__id=req.user.id)
        user_form = UpdateUserForm(req.POST or None, req.FILES or None ,instance=curr_user)
        profile_form = ProfileImageForm(req.POST or None,req.FILES or None, instance=profile_user)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(req,curr_user)
            messages.success(req,"Profile Updated!")
            return redirect('/profile/%d'%req.user.id)
        return render(req,"update_user.html",{"user_form":user_form,"profile_form":profile_form})
    else:
        messages.success(req,"You must be logged in to view this page!")
        return redirect('home')


def likes(req,pk):
    if req.user.is_authenticated:
        talks = get_object_or_404(Talk,id=pk)
        if talks.likes.filter(id = req.user.id):
            talks.likes.remove(req.user)
        else:
            talks.likes.add(req.user)
        return redirect(req.META.get("HTTP_REFERER"))
    else:
        messages.success(req,"You must be logged in to ❤️ this talks!")
        return redirect('home')
    

def share(req,pk):
    talks = get_object_or_404(Talk,id=pk)
    if talks:
        return render(req,"show_tweet.html",{"talks":talks})
    else:
        messages.success(req,"Tweet Does Not Exist or Deleted!")
        return redirect('home')
    
