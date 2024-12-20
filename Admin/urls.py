from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('home/', views.home,name='home'),
    path('users_view/',views.users_view,name='users_view'),
    path('deleteuser/<int:user_id>', views.deleteuser, name='deleteuser'),
    path('logout/', views.Logout, name='logout'),
    path('blogsview/', views.blogsview, name='blogsview'),
    path('blogdelete/<int:blog_id>', views.blogdelete, name='blog_delete'),

    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)