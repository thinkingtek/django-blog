from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView, View, RedirectView
from django.utils.decorators import method_decorator
from ..models import Post, Category, PostView
from django.db.models import Q, Count
from ..forms import *
from ..decorators import *
from account.models import User
from django.contrib.auth import login
