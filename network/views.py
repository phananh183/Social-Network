import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Following


def index(request):
    return render(request, "network/index.html", {
        "posts": Post.objects.order_by('-timestamp').all()
    })

def showPost(request):
    posts = Post.objects.order_by('-timestamp').all()
    return JsonResponse([post.serialize() for post in posts], safe=False)

def showPostByProfile(request, profile_id):
    profile = User.objects.get(id=profile_id)
    posts = Post.objects.filter(poster=profile).order_by('-timestamp').all()
    return JsonResponse([post.serialize() for post in posts], safe=False)

def followingData(request):

    #get get list of people user is following
    followings = Following.objects.filter(user=request.user)
    
    #add all posts of people user is following
    posts = []
    for follow in followings:
        for post in list(Post.objects.filter(poster=follow.followed)):
            posts.append(post)
    
    #sort post by timestamp, most recent post first
    posts.sort(key=lambda x: x.timestamp, reverse=True)
    
    return JsonResponse([post.serialize() for post in posts], safe=False)

def following(request):
    return render(request, "network/following.html")



def profile(request, profile_id):
    profile = User.objects.get(pk=profile_id)

    #check if user is following profile
    toggleFollow = Following.objects.filter(user=request.user).filter(followed=profile).exists()
    
    #number of users that account is follwing
    following = len(Following.objects.filter(user=profile))

    #number of followers that account has
    followers = len(Following.objects.filter(followed=profile))
    return render(request, "network/profile.html", {
        "profile": profile,
        "following": following,
        "followers": followers,
        "toggleFollow": toggleFollow
    })

@csrf_exempt
@login_required
def toggleFollow(request, profile_id):
    #Toggle follow must be done through a POST request
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)

    profile = User.objects.get(id=profile_id)
    followObject = Following.objects.filter(user=request.user).filter(followed=profile)
    
    if followObject.exists():
        followObject.delete()
        return JsonResponse({"meassage": "Toggled follow." }, status=201)

    else:
        newFollow = Following(user=request.user, followed=profile)
        newFollow.save()
        return JsonResponse({"meassage": "Toggled follow." }, status=201)

@csrf_exempt
@login_required
def post(request):
    #Post a new post must be done through a POST request
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)

    #Get post content
    data = json.loads(request.body)
    poster = request.user
    content = data.get("content","")
    
    #Create a new post
    newPost = Post(
        poster = poster,
        content = content
    )
    newPost.save()
    return JsonResponse({"message": "New post created successfully."}, status=201)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
