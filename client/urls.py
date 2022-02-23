from django.urls import path, re_path
from .views import *

urlpatterns = [
    #Index and search page url
    path('',Index_View.as_view(),name='index'),
    path('search',Search_View.as_view(),name='search'),

    #video player url
    path('video/<int:pk>/',Video_View.as_view(),name='video'),
        #Like and dislike urls
    path('video/<int:pk>/like/',Like_View.as_view(),name='like'),
    path('video/<int:pk>/dislike/',Dislike_View.as_view(),name='dislike'),
        # comment
    path('video/<int:pk>/comment',CommentView.as_view(),name='comment'),
    
    #Channel urls
    path('channel/<int:pk>',ChannelView.as_view(),name='channel'),
    path('channel/subscription/<int:pk>',ChannelSubscription.as_view(),name='channel_subscription'),
    path('channel/userchannel',UserChannelView.as_view(),name='user_channel'),
    path('channel/video/upload',VideoUpload.as_view(),name='video_upload'),

    #Authentications urls
    path('auth/login',LoginView.as_view(),name='login'),
    path('auth/registration',RegistrationView.as_view(),name='registration'),
    path('auth/logout',LogoutView,name='logout')
    
]