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
from Blog import class_based_views as cb_views
from django.conf import settings
from django.conf.urls.static import static
from Blog import forms as F
from django.contrib.auth.decorators import login_required






urlpatterns = [
    #admin
    path('admin/', admin.site.urls),
    #auth
    path('auth/login/', auth_views.login_page, name='login_page'),
    path('auth/signup/', auth_views.signup_page, name='signup_page'),
    path('auth/logout/', auth_views.logout_page, name='logout_page'),
    #content_creation
    path('blog/ticket_creation/',cb_views.Content_Create.as_view(ticket_form = F.TicketForm), name='ticket_creation'),
    path('blog/ticket/<int:ticket_id>/reply/', cb_views.Content_Create.as_view(review_form = F.ReviewForm), name='reply'),
    path('blog/review_creation/', cb_views.Content_Create.as_view(review_form = F.ReviewForm,ticket_form = F.TicketForm), name='review_creation'),

    #post management
    path('blog/ticket/<int:ticket_id>/edit',login_required(cb_views.Content_Edit.as_view()),name='edit'),

    path('blog/ticket/<int:ticket_id>/delete',login_required(cb_views.delete_content.as_view()),name='delete'),

    path('blog/review/<int:review_id>/delete',login_required(cb_views.delete_content.as_view()),name='delete'),
    
    #content page
    path('blog/flux/', login_required(cb_views.Content_page.as_view(feed=True)), name='flux'),
    path('', login_required(cb_views.Content_page.as_view(feed=True)), name=''),
    path('blog/post/', login_required(cb_views.Content_page.as_view(feed=False , template_url="Blog/post.html")), name='post'),
    
    #follow and unefollow
    path('blog/follow/', login_required(cb_views.Follow.as_view()),name='follow'),
    path('blog/follow/<int:user_id>/unfollow', login_required(cb_views.Follow.as_view()),name='unfollow'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
