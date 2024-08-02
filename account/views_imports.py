from django.urls import reverse_lazy
from .mixins import RedirectAuthUser
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetDoneView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from .forms import *
from blog.models import Post, Comment
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView, View
from .decorators import *
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponse, HttpResponseRedirect
from datetime import timedelta, date
# from .models import User
