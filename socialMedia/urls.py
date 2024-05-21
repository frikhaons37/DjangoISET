
from django.contrib import admin

from django.conf.urls.static import static

from django.conf import settings
from django.urls import path, include
from django.views.generic import TemplateView,RedirectView
from posts import views

urlpatterns = [
    path("", views.index,name='home'),
    path("", include("accounts.urls")),
    path("", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path('friend/',include("friend.urls")),

    path('posts/', include("posts.urls")),
    path('groups/', include("groups.urls")),
    path('messages/', include("msgnotifications.urls")),

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('',TemplateView.as_view(template_name='404.html')),
]