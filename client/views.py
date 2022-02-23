from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import TemplateView,ListView,DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, get_user_model, login, logout, views
from django.contrib import messages
from django.db.models import Q
from django.views import View
from .Utils import LoginRequiredView
from .models import *
from .forms import ProfilePicForm
from django.contrib import messages
User = get_user_model()
#index view for homepage and search view for search result page
class Index_View(ListView):
    model = Video
    template_name = 'index.html'
    query_set = Video.objects.all().select_related('user')[:50]
    context_object_name = 'videos'

class Search_View(View):
    def get(self,request):
        q=request.GET['q']
        context={}
        context['videos'] = Video.objects.all().filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(tags__icontains=q)).select_related('user')[:50]
        if not len(context['videos']):
            context['error']='No result found !'
        return render(request,'index.html',context)

#view for video player page
class Video_View(DetailView):
    model = Video
    template_name = 'video.html'
    context_object_name = 'video'
    
    def get_context_data(self,**kwargs):
        context = super(Video_View,self).get_context_data(**kwargs)
        context['likes'] = LikeDislike.objects.all().filter(video=self.object,like=True).count()
        context['dislikes'] = LikeDislike.objects.all().filter(video=self.object,dislike=True).count()
        if self.request.user.is_authenticated:
            likedordisliked = LikeDislike.objects.all().filter(video=self.object,user=self.request.user)
            if len(likedordisliked):
                context['liked']=likedordisliked[0].like
                context['disliked']=likedordisliked[0].dislike
        # get comments
        context['comments'] = Comment.objects.all().order_by('-created_at').select_related('user')[:30]
        # Get related videos
        tags = list(map(str,self.object.tags.split(',')))
        related = None
        for tag in tags :
            videos = Video.objects.all().filter(tags__icontains=tag).exclude(id=self.object.id).select_related('user')
            if related==None:
                related = videos
            else:
                related.union(videos)
        context['related'] = related
        return context

    #View for like and dislike a video
class Like_View(LoginRequiredView):
    def get(self,request,**kwargs):
        like = LikeDislike.objects.get_or_create(user=request.user,video=Video.objects.get(id=kwargs['pk']))[0]
        like.like = True
        like.dislike = False
        like.save()
        return redirect(request.META["HTTP_REFERER"])

class Dislike_View(LoginRequiredView):
    def get(self,request,**kwargs):
        dislike = LikeDislike.objects.get_or_create(user=request.user,video=Video.objects.get(id=kwargs['pk']))[0]
        dislike.like = False
        dislike.dislike = True
        dislike.save()
        return redirect(request.META["HTTP_REFERER"])

    # View for comment on video
class CommentView(LoginRequiredView):
    def post(self,request,**kwargs):
        comment = Comment()
        comment.user = request.user
        comment.video = get_object_or_404(Video,id=kwargs['pk'])
        comment.comment = request.POST['comment']
        comment.save()
        return redirect(request.META['HTTP_REFERER'])



#Channel views
    # Any channel view by both logged and annonyms user
class ChannelView(DetailView):
    template_name = 'channel.html'
    model = User
    context_object_name = 'channel'
    def get_context_data(self,**kwargs):
        context = super(ChannelView,self).get_context_data(**kwargs)
        context['videos'] = Video.objects.all().filter(user=self.object)
        context['subscription'] = Subscription.objects.all().filter(channel=self.object.id).count()
        # Check if current user is subscribed to this channel
        if self.request.user.is_authenticated:
            check_subscribed = Subscription.objects.all().filter(channel=self.object.id,subscriber=self.request.user)
            if len(check_subscribed):
                context['subscribed']=True
        return context

    # Channel view for only user own channel
class UserChannelView(LoginRequiredView):
    template_name = 'user_channel.html'
    def get(self,request):
        subscription = Subscription.objects.all().filter(channel=request.user.id).count()
        videos = Video.objects.all().filter(user=request.user)
        return render(request,self.template_name,{'videos':videos,'subscription':subscription})
    def post(self,request):
        if request.FILES.get('profile_pic') :
            form = ProfilePicForm(request.POST,request.FILES)
            if form.is_valid():
                request.user.profile_pic = request.FILES['profile_pic']
                request.user.save()
        if request.POST.get('channel-name') :
            request.user.channel_name = request.POST.get('channel-name')
            request.user.save()
        return redirect(reverse('user_channel'))

    # Subscribe Channel
class ChannelSubscription(LoginRequiredView):
    def get(self,request,**kwargs):
        channel =  get_object_or_404(User,id=kwargs['pk'])
        subscription = Subscription.objects.get_or_create(channel=channel.id,subscriber=request.user)
        return redirect(reverse('channel',kwargs={'pk':channel.id}))

    # Video Upload
class VideoUpload(LoginRequiredView):
    template_name = 'upload.html'
    def get(self,request):
        return render(request, self.template_name)
    def post(self,request):
        if not request.user.channel_name:
            messages.error(request,'Please set your channel name and profile pic first')
            return redirect(reverse('user_channel'))
        else:
            video = Video()
            video.title = request.POST['title']
            video.user = request.user
            video.description = request.POST['description']
            video.video = request.FILES['video']
            video.thumbnail = request.FILES['thumbnail']
            video.tags = request.POST['tags']
            video.save()
            return redirect(reverse('user_channel'))




#Authentication view
class LoginView(View):
    template_name='login.html'
    def get(self,request):
        if request.user.is_authenticated:
            return redirect(reverse('index'))
        return render(request,self.template_name)

    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user != None :
            login(request, user)
            next = request.GET.get('next')
            if(next):
                return redirect(next)
            return redirect(reverse('index'))
        messages.error(
            request, 'Invalid Login or Your account is deactivated!')
        return redirect(reverse('login'))
class RegistrationView(View):
    template_name='registration.html'
    def get(self,request):
        if request.user.is_authenticated:
            return redirect(reverse('index'))
        return render(request,self.template_name)
    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        error = 0
        if(email == ""):
            error += 1
            messages.error(request, "Email cannot be Empty.")

        else:
            try:
                match = User.objects.get(email=email)
                error += 1
                messages.error(request, "Email already exists.")
            except:
                pass
        if(password != password2):
            error += 1
            messages.error(request, "Confirm password doesn't match.")

        if(len(password) < 8):
            error += 1
            messages.error(request, "Password Length not less than 8.")

        if(not error):
            user = User.objects.create_user(email, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.is_active = False
            user.save()
            login(request,user)
            return reverse(request.META['HTTP_REFERER'])
        return redirect('registration')
def LogoutView(request):
    logout(request)
    return redirect(reverse('login'))