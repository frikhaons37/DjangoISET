
from django.urls import path
from .import views
from .views import PostUpdateView, ajout_reservation
from .views import PostDeleteView



urlpatterns = [
    path("", views.index,name="index"),
    path('edit/<int:pk>/', PostUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='delete'),
    path("view/<int:id>", views.view,name="view"),
    path("view/<int:id>/comment",views.AddCommentView,name="add_comment"),
    path("comment/<int:id>",views.delComment,name="del_comment"),
    path("like/",views.like_post,name="like-post"),
    path('view/<int:id>/postlikes/', views.post_likes, name='post-likes'),
    #reservation
    path('ajout-reservation/<int:post_id>/', ajout_reservation, name='ajout_reservation'),
    
]
