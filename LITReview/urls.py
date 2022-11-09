"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Authenticate import views as auth_views
from Blog import views as blog_views
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login/', auth_views.login_page, name='login_page'),
    path('auth/signup/', auth_views.signup_page, name='signup_page'),
    path('auth/logout/', auth_views.logout_page, name='logout_page'),
    path('blog/ticket_creation/', blog_views.ticket_create, name='ticket_creation'),
    path('', blog_views.flux, name='flux'),
    path('blog/post/', blog_views.post,name='post'),
    path('blog/ticket/<int:ticket_id>/edit',blog_views.edit,name='edit'),
    path('blog/ticket/<int:ticket_id>/delete',blog_views.delete,name='review'),
    path('blog/follow/', blog_views.follow_page,name='follow'),
    path('blog/follow/<int:user_id>/unfollow', blog_views.unfollow,name='unfollow'),
    path('blog/flux/', blog_views.flux, name='flux'),
    path('blog/ticket/<int:ticket_id>/reply/', blog_views.review_create, name='reply'),
    path('blog/review_creation/', blog_views.review_create, name='review_creation')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)