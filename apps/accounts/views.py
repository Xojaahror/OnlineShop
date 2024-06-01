from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .forms import CustomAuthForm, UserCreateForm

# Create your views here.
class LoginView(View):
    form_class = CustomAuthForm
    def get(self, request):
        url = request.GET.get('next', 'products:home')
        # print(request.GET.next, "\n#############################################")
        if request.user.is_authenticated:
            return redirect('products:home')
        else:
            return render(request, "accounts/login.html", {'login_form': self.form_class})
        
    def post(self, request):
        # url = request.META.get('HTTP_REFERER')
        # print(url, "\n##################################################3")
        url = request.GET.get('next', 'products:home')

        login_form = self.form_class(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect(url)
        else:
            messages.error(request, 'Invalid data!!!')
            return render(request, 'accounts/login.html', {"login_form" : login_form})

class LogoutView(View):
    def get(self, request):
        url = request.META.get('HTTP_REFERER')
        logout(request)
        messages.info(request, 'You successfully logged out.')
        if url:
            return redirect(url)
        else:
            return redirect('products:home')
        
class RegisterView(View):
    form_class = UserCreateForm
    def get(self, request):
        return render(request, 'accounts/register.html', {'form':self.form_class})
    
    def post(self, request):
        create_form = self.form_class(data=request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect('login')
        else:
            messages.error(request, f"{create_form.errors}")
            return render(request, 'accounts/register.html', {'form':create_form})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/profile.html', {})
