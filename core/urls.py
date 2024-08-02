"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from account.views import *

urlpatterns = [
    path('', include('blog.urls', namespace='blog')),
    path('contact-us/', Contact.as_view(),
         name='contact-us'),
    path('admin/', admin.site.urls),
    path('delete-user/', deactivateUser, name='deactivate-user'),
    path('profile/', profile, name='profile'),

    #     Auth links
    path('login/', UserLoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', userLogout, name='logout'),
    path('sign-In/', register, name='signin'),

    path('activate/<slug:uidb64>/<slug:token>)/', activate, name='activate'),
    path('password-reset/', ResetPassword.as_view(), name='password-reset'),

    path('password-reset-confirm/<uidb64>/<token>/',
         ResetPasswordConfirm.as_view(), name='password_reset_confirm'),


    path('password-reset-done/', ResetDoneView.as_view(),
         name='password-reset-done'),

    path('password-reset-complete/', ResetPasswordComplete.as_view(),
         name='password-reset-complete'),

    path('password-change/', PasswordChange.as_view(),
         name='password-change'),
    path('password-change-done/', PasswordChangeDone.as_view(),
         name='password-change-done'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Blog Webapp'
admin.site.index_title = 'Manage the Site'
