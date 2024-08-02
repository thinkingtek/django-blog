from .views_imports import *
User = get_user_model()


@redirect_authenticated_user
def register(request):
    form = UserRegForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.username = form.cleaned_data.get(
                'username').lower()
            form.instance.email = form.cleaned_data.get(
                'email').lower()
            email = form.cleaned_data.get('email').lower()
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string('account/email_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            # user.email_user(subject=subject, message=message)
            # I think this is used for production
            send_email = EmailMessage(subject, message, to=[email])
            send_email.send()
            return render(request, 'account/email_sent.html')

    context = {
        'title': 'Sign-up',
        'form': form
    }
    return render(request, 'account/register.html', context)


@login_required
def profile(request):
    username = request.user.username
    email = request.user.email
    u_form = UserUpdateForm(request.POST or None, instance=request.user)
    p_form = ProfileUpdateForm(
        request.POST or None, request.FILES, instance=request.user.profile)
    if request.method == 'POST':
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    context = {
        'email': email,
        'username': username,
        'title': f'{username} | Profile',
        'u_form': u_form,
        'p_form': p_form,
        'profile_active': True
    }
    return render(request, 'account/profile.html', context)


@login_required
def deactivateUser(request, *args, **kwargs):
    user = User.objects.get(username=request.user)
    user_posts = Post.objects.filter(author=user)
    user_comments = Comment.objects.filter(user=user)
    if user:
        user.is_active = False
        user.save()
        user_posts.delete()
        user_comments.delete()
        logout(request)
        messages.info(request, 'Account deleted')
        return redirect('login')


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'

    def form_invalid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        return super(UserLoginView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Login"
        return context


@redirect_unauthenticated_user
def userLogout(request):
    messages.info(
        request, f"{request.user.username} You have successfully logged out")
    logout(request)
    return redirect("login")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, f'Account successfully activated {user.username} you can now login')
        return redirect('login')
    else:
        return render(request, 'account/activation_invalid.html')


class PasswordChange(PasswordChangeView):
    template_name = 'account/password_change.html'
    success_url = reverse_lazy('password-change-done')


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'account/password_change_done.html'
    success_url = reverse_lazy('password-change-done')


class ResetPassword(RedirectAuthUser, SuccessMessageMixin, PasswordResetView):
    template_name = 'account/password_reset.html'
    form_class = PasswordFormReset
    success_url = reverse_lazy('password-reset')
    success_message = 'An instruction has been sent to your email with  to reset your account password'


class ResetPasswordConfirm(RedirectAuthUser, PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('password-reset-complete')


class ResetPasswordComplete(RedirectAuthUser, PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'


class ResetDoneView(RedirectAuthUser, PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'
    # This view isnt in use because i did a redirect to the same view that sent the email address which is PasswordResetView. But its just here just incase i decide to use it


class Contact(FormView):
    form_class = ContactForm
    template_name = 'account/contact-form.html'
    success_url = reverse_lazy('contact-us')

    def form_valid(self, form):
        first_name = form.cleaned_data.get('first_name').title()
        last_name = form.cleaned_data.get('last_name').title()
        email = form.cleaned_data.get('email').lower()
        message = form.cleaned_data.get('message')
        full_name = f'{first_name} {last_name}'

        full_message = f"""
         Recieved message below from {full_name}, {email}
         ____________________________________
         {message}
        """
        send_mail(
            subject='Recieved contact us information',
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFY_EMAIL]
        )
        messages.info(
            self.request, f"Thanks for getting in touch with us {full_name}, we receieved your message.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Web blog | Contact Us'
        context["contact_active"] = True
        return context
