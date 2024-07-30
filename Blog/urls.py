from django.urls import path
from . import views


urlpatterns = [
    path("",views.StartPage.as_view(),name="start-page"),
    path("posts",views.Posts.as_view(),name="posts-page"),
    path("posts/<slug:slug>",views.PostDetail.as_view(),name="post-detail-page"),
    path('read-later',views.ReadLater.as_view(),name='read-later'),
    path('add-post',views.AddPost.as_view(),name='add-post')
]
