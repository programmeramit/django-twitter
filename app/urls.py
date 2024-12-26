
from .views import home,profile,edit,delete_post,like,comment,user,add_bookmark,bookmarks,profile_images,profile_videos,search,follow
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",home,name="home"),
    path('accounts/', include('allauth.urls')),
    path('profile/',profile,name="profile"),
    path('profile/edit/<int:id>',edit,name="edit"),
    path('profile/post/<int:post_id>/delete/', delete_post, name='delete_post'),
    path('like/<int:id>/',like,name="like"),
    path('comment/<int:id>',comment,name="comment"),
    path('user/<int:id>',user,name="user"),
    path('bookmark/<int:id>',add_bookmark,name="add_bookmark"),
    path('bookmarks',bookmarks,name="bookmarks"),
    path('profile_images',profile_images,name="profile_images"),
    path('profile_videos',profile_videos,name="profile_videos"),
    path('search/',search,name="search"),
    path('follow/<int:id>',follow,name="follow")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


