from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView,LogoutView
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserUpdateForm,ChangePasswordForm
from django.urls import reverse_lazy
from django.contrib.auth import login,logout
from django.views import View
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

# Create your views here.


class UserRegisterView(FormView):
    template_name='accounts/register.html'
    form_class=UserRegistrationForm
    success_url=reverse_lazy('login')
    
    
    def form_valid(self, form):
        user=form.save()
        messages.success(self.request,'Account create successfully')
        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name='accounts/login.html'
    
    def get_success_url(self) :
        messages.success(self.request,'Log in successfully')
        return reverse_lazy('profile')
    
class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')
    

class UserBankAccountUpdateView(View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  
        return render(request, self.template_name, {'form': form})
    

@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password was successfully updated!')
            
      
            message = render_to_string('accounts/password_change_email.html', {'user': user})
            subject = 'Password Change Confirmation'
            send_email = EmailMultiAlternatives(subject, '', to=[user.email])
            send_email.attach_alternative(message, "text/html")
            send_email.send()
            
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ChangePasswordForm(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})