from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .forms import TweetForm
import time
from django.db.models import Count
import re 
from django.contrib.auth.decorators import login_required
from .models import Tweet,HashTag,Like,Comment,Bookmark,Follow,Profile
from django.contrib.auth.models import User
from .forms import EditForm
import plotly.express as px


@login_required
def home(request):
    if request.method == 'POST':
        tweet = request.POST.get('text')
        file = request.FILES.get('file')
        hashtags = re.findall(r'#\w+', tweet)
    
        user = request.user

        post = Tweet(user=request.user,content=tweet,media=file)
        post.save()
        for tag in hashtags:
            tag_name = tag[1:]
            hashtag, created = HashTag.objects.get_or_create(name=tag_name)
            post.hashtags.add(hashtag)

        
        return redirect('home')

    else:
        form = TweetForm()

    posts = Tweet.objects.all()
    hashtags = HashTag.objects.annotate(post_count=Count('tweet')).order_by('-post_count')[:5]

    all_users = User.objects.exclude(id=request.user.id)
        
    following = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
        
    users = all_users.exclude(id__in=following)

    
    
    print(users)

    return render(request,"index.html",{'form': form,'posts':posts,"hashtags":hashtags,"users":users})


def profile(request):
    user = request.user
    name = user.username
    email = user.email
    first_name= user.first_name
    last_name= user.last_name
    top_hashtags = HashTag.objects.all().distinct().count()

    data = {
        "Category": ["A", "B", "C", "D"],
        "Values": [10, 20, 30, 40]
    }

    # Create a Plotly figure
    fig = px.line(data, x="Category", y="Values", title="Likes")

    fig.update_layout(
    title=dict(font=dict(size=24, color="blue")),
    paper_bgcolor="lightgray",
    plot_bgcolor="white",
    legend=dict(bgcolor="rgba(255,255,255,0.8)", bordercolor="gray"),
)


    # Convert the figure to HTML
    graph_html = fig.to_html(full_html=False)

    get_follow =  User.objects.get(id=request.user.id)
    followers = Follow.objects.exclude(follower=request.user)
    posts = Tweet.objects.filter(user=request.user)
    hashtags = HashTag.objects.annotate(post_count=Count('tweet')).order_by('-post_count')[:5]

    context = {"name":name,"email":email,"first_name":first_name,"last_name":last_name,"posts":posts,"hashtags":hashtags,"user":get_follow,"graph_html":graph_html}
    return render(request,"profile.html",context)

@login_required
def edit(request, id):
    form_data = get_object_or_404(Tweet,id=id)

    if request.method == "POST":
        if request.FILES.get('file'):
            form_data.media = request.FILES.get('file')

        if request.POST.get('content'):

            form_data.content = request.POST.get('content')

        form_data.save()
        
        

        return redirect('profile')
    print(form_data)

    return render(request, "edit.html", {"form": form_data})





@login_required  
def delete_post(request, post_id):
    post = get_object_or_404(Tweet, id=post_id)

    post.delete() 
    return redirect('profile') 

@login_required
def like(request,id):
    post = get_object_or_404(Tweet,id=id)
    like,created = Like.objects.get_or_create(user=request.user,post=post)
    if not created:
        like.delete()
    return redirect('home')

@login_required
def comment(request,id):


    return redirect('comment')

def comment(request,id):
    post = Tweet.objects.get(id=id)
    comment = request.POST.get('comment')
    if request.method == "POST":
        Comment.objects.create(user=request.user,content=comment,post=post)
        return redirect('comment',id)
    return render(request,'comment.html',{"post":post})
    

def user(request,id):
    user = User.objects.get(id=id)

    if request.method == "POST":
            Follow.objects.create(follower=request.user,following=user)
            return redirect('user',id)


    name = user.username
    email = user.email
    first_name= user.first_name
    last_name= user.last_name
    top_hashtags = HashTag.objects.all().distinct().count()

    get_follow =  User.objects.get(id=id)
    posts = Tweet.objects.filter(user=user)
    hashtags = HashTag.objects.annotate(post_count=Count('tweet')).order_by('-post_count')[:5]
    follow_or = "Follow"
    users = request.user.following.all()
    for id in users:
        if user.id == id.following_id:
            follow_or="Following"

  


    context = {"name":name,"email":email,"first_name":first_name,"last_name":last_name,"posts":posts,"hashtags":hashtags,"user":get_follow,"person":user,"follow_or":follow_or}
    return render(request,"user.html",context)

@login_required
def add_bookmark(request,id):
    post = Tweet.objects.get(id=id)
    Bookmark.objects.create(user=request.user,post=post)
    return redirect('home')

def bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user)
    return render(request,"bookmark.html",{"bookmarks":bookmarks})
    

def profile_images(request):
    get_image_tweets = Tweet.objects.filter(user=request.user)
    return render(request,"profile_images.html",{"posts":get_image_tweets})

def profile_videos(request):
    get_image_tweets = Tweet.objects.filter(user=request.user)
    return render(request,"profile_videos.html",{"posts":get_image_tweets})

def search(request):
    if request.method == "POST":
        text = request.POST.get("user")
        results = User.objects.filter(first_name__startswith = text).all()
        return render(request,"search.html",{"results":results})
        
    return render(request,"search.html")


def follow(request,id):
    user = User.objects.get(id=id)
    Follow.objects.create(follower=request.user,following=user)

    return redirect('home')

def edit_user(request):
    user = User.objects.get(id=request.user.id)

    if request.method == "POST":
        user.username= request.POST.get("username")
        user.first_name =  request.POST.get("first_name")
        user.last_name= request.POST.get("last_name")
        
        if request.FILES.get("profile_pic"):
            user.profile.profile_pic = request.FILES.get("profile_pic")
        print(request.FILES.get("profile_pic"))

        return redirect('profile')
    return render(request,"profile_edit.html",{"data":user})

