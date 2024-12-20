from django.urls import path
from . import views
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [

    path('register/', views.user_registration, name='register'),
    path('login/', views.loginpage, name='login'),
    path('user_view/', views.user_view, name='user_view'),
    path('Guesthome/', views.Guesthome, name='Guesthome'),
    path('blogs/', views.blogs, name='blogs'),
    path('uploadblogs/', views.uploadblogs, name='uploadblogs'),
    path('photo/', views.photo, name='photo'),
    path('userhome/', views.userhome, name='userhome'),
    path('profile/', views.profile, name='profile'),
    path('updateprofile/', views.updateprofile, name='updateprofile'),
    path('deleteblog/<int:blog_id>/', views.deleteblog, name='delete'),
    path('comment/', views.comment, name='comment'),
    path('logout/', views.Logout, name='logout'),
    path('updateblog/<int:blog_id>/', views.updateblog, name='updateblog'),
    path('view_comments/<int:blog_id>/', views.view_comments, name='view_comments'),

                  #path('update_profile/', views.update_profile, name='update_profile'),  # Fixed this line

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)