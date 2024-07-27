# from django.shortcuts import render

# # Create your views here.
# from django.shortcuts import render, redirect
# from .forms import RegisterForm
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required

# # Create your views here.

# def index(request):
#     return render(request, 'index.html')

# def register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return render(request, 'login.html', {'success': "Registration successful. Please login."})
#         else:
#             error_message = form.errors.as_text()
#             return render(request, 'register.html', {'error': error_message})

#     return render(request, 'register.html')


# def login_view(request):
#     if request.method=="POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect("/dashboard")
#         else:
#             return render(request, 'login.html', {'error': "Invalid credentials. Please try again."})

#     return render(request, 'login.html')

# @login_required
# def dashboard(request):
#     return render(request, 'dashboard.html', {'name': request.user.first_name})

# @login_required
# def videocall(request):
#     return render(request, 'videocall.html', {'name': request.user.first_name + " " + request.user.last_name})

# @login_required
# def logout_view(request):
#     logout(request)
#     return redirect("/login")

# @login_required
# def join_room(request):
#     if request.method == 'POST':
#         roomID = request.POST['roomID']
#         return redirect("/meeting?roomID=" + roomID)
#     return render(request, 'joinroom.html')
from itertools import chain
from  django . shortcuts  import  get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . models import  Followers, LikePost, Post, Profile
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from .models import Room, Message
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.conf import settings

def signup(request):
 try:
    if request.method == 'POST':
        fnm=request.POST.get('fnm')
        emailid=request.POST.get('emailid')
        pwd=request.POST.get('pwd')
        print(fnm,emailid,pwd)
        my_user=User.objects.create_user(fnm,emailid,pwd)
        my_user.save()
        user_model = User.objects.get(username=fnm)
        new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
        new_profile.save()
        if my_user is not None:
            login(request,my_user)
            return redirect('/')
        return redirect('/loginn')
    
        
 except:
        invalid="User already exists"
        return render(request, 'signup.html',{'invalid':invalid})
  
    
 return render(request, 'signup.html')
        
     
        
        
        
        
    

def loginn(request):
 
  if request.method == 'POST':
        fnm=request.POST.get('fnm')
        pwd=request.POST.get('pwd')
        print(fnm,pwd)
        userr=authenticate(request,username=fnm,password=pwd)
        if userr is not None:
            login(request,userr)
            return redirect('/')
        
 
        invalid="Invalid Credentials"
        return render(request, 'loginn.html',{'invalid':invalid})
               
  return render(request, 'loginn.html')

@login_required(login_url='/loginn')
def logoutt(request):
    logout(request)
    return redirect('/loginn')



@login_required(login_url='/loginn')
def home(request):
    
    following_users = Followers.objects.filter(follower=request.user.username).values_list('user', flat=True)

    
    post = Post.objects.filter(Q(user=request.user.username) | Q(user__in=following_users)).order_by('-created_at')

    profile = Profile.objects.get(user=request.user)

    context = {
        'post': post,
        'profile': profile,
    }
    return render(request, 'main.html',context)
    


@login_required(login_url='/loginn')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='/loginn')
def likes(request, id):
    if request.method == 'GET':
        username = request.user.username
        post = get_object_or_404(Post, id=id)

        like_filter = LikePost.objects.filter(post_id=id, username=username).first()

        if like_filter is None:
            new_like = LikePost.objects.create(post_id=id, username=username)
            post.no_of_likes = post.no_of_likes + 1
        else:
            like_filter.delete()
            post.no_of_likes = post.no_of_likes - 1

        post.save()

        # Generate the URL for the current post's detail page
        print(post.id)

        # Redirect back to the post's detail page
        return redirect('/#'+id)
    
@login_required(login_url='/loginn')
def explore(request):
    post=Post.objects.all().order_by('-created_at')
    profile = Profile.objects.get(user=request.user)

    context={
        'post':post,
        'profile':profile
        
    }
    return render(request, 'explore.html',context)
    
@login_required(login_url='/loginn')
def profile(request,id_user):
    user_object = User.objects.get(username=id_user)
    print(user_object)
    profile = Profile.objects.get(user=request.user)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=id_user).order_by('-created_at')
    user_post_length = len(user_posts)

    follower = request.user.username
    user = id_user
    
    if Followers.objects.filter(follower=follower, user=user).first():
        follow_unfollow = 'Unfollow'
    else:
        follow_unfollow = 'Follow'

    user_followers = len(Followers.objects.filter(user=id_user))
    user_following = len(Followers.objects.filter(follower=id_user))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'profile': profile,
        'follow_unfollow':follow_unfollow,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    
    
    if request.user.username == id_user:
        if request.method == 'POST':
            if request.FILES.get('image') == None:
             image = user_profile.profileimg
             bio = request.POST['bio']
             location = request.POST['location']

             user_profile.profileimg = image
             user_profile.bio = bio
             user_profile.location = location
             user_profile.save()
            if request.FILES.get('image') != None:
             image = request.FILES.get('image')
             bio = request.POST['bio']
             location = request.POST['location']

             user_profile.profileimg = image
             user_profile.bio = bio
             user_profile.location = location
             user_profile.save()
            

            return redirect('/profile/'+id_user)
        else:
            return render(request, 'profile.html', context)
    return render(request, 'profile.html', context)

@login_required(login_url='/loginn')
def delete(request, id):
    post = Post.objects.get(id=id)
    post.delete()

    return redirect('/profile/'+ request.user.username)


@login_required(login_url='/loginn')
def search_results(request):
    query = request.GET.get('q')

    users = Profile.objects.filter(user__username__icontains=query)
    posts = Post.objects.filter(caption__icontains=query)

    context = {
        'query': query,
        'users': users,
        'posts': posts,
    }
    return render(request, 'search_user.html', context)

def home_post(request,id):
    post=Post.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    context={
        'post':post,
        'profile':profile
    }
    return render(request, 'main.html',context)



def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if Followers.objects.filter(follower=follower, user=user).first():
            delete_follower = Followers.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = Followers.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

def wellnessWizard(request):
    return render(request, 'wellnesswizard.html')

def dashboard(request):
    return render(request, 'dashboard.html', {'name': request.user.first_name})

def dietplanner(request):
    return render(request,'dietplanner.html')

def videocall(request):
    return render(request, 'videocall.html', {'name': request.user.first_name + " " + request.user.last_name})

def logout_view(request):
    logout(request)
    return redirect("/login")
def esignup(request):
    return render(request, 'esignup.html')

def join_room(request):
    if request.method == 'POST':
        roomID = request.POST.get('roomID')
        if roomID is None:
            return render(request, 'joinroom.html', {'error': 'Room ID is required'})
        return redirect(f"/meeting?roomID={roomID}")
        roomID = request.POST['roomID']
        return redirect("/meeting?roomID=" + roomID)
    return render(request, 'joinroom.html')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json

class ChatView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            user_message = body.get('message')

            response = requests.post(
                'https://chatapi.akash.network/api/v1/completions',
                headers={
                    'Authorization': 'Bearer sk-ZZAOd9NUGtvNoyKmc-tnrw',
                    'Content-Type': 'application/json',
                },
                json={
                    'model': 'llama3-8b',
                    'messages': [
                        {'role': 'user', 'content': user_message},
                    ],
                }
            )

            response_data = response.json()
            bot_response = response_data['choices'][0]['message']['content'].strip()

            return JsonResponse({'response': bot_response})

        except Exception as e:
            return JsonResponse({'error': 'An error occurred'}, status=500)
def hhome(request):
    return render(request, 'hhome.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})

