from django.urls import path, include
from streamapp import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.signin, name='login'),
    path('register', views.register, name='register'),
    path('signout', views.signout, name='signout'), 
    path('mainpage', views.mainpage, name='mainpage'),
    path('about', views.about, name='about'),
    path('course', views.courses, name='course'),
    path('contact', views.contact, name='contact'),
    path('choose_sub',views.choose_sub, name='choose_sub'),
    path('profile',views.profile, name='profile'),
    path('level',views.level, name='level'),







    path('exampage', views.exampage, name='exampage'),
    path('subject', views.coursess, name='course'),    
    #exampage
    path('test', views.test, name='test'),
    
    
    
    #mcq's
    path('startmock', views.startmock, name='startmock'),












    # path('record_facial_data', views.record_facial_data, name='record_facial_data'),
    path('video_feed', views.video_feed, name='video_feed'),
    # path('video_feed', views.video_feed, name='video_feed'),
    # path('webcam_feed', views.webcam_feed, name='webcam_feed'),
    # path('mask_feed', views.mask_feed, name='mask_feed'),
	# path('livecam_feed', views.livecam_feed, name='livecam_feed'),
    ]
