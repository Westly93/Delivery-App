from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm
from django.contrib import messages

class UserRegisterView(View):
    def get(self, request):
        form= UserRegistrationForm()
        context={
            'title': 'User Registration',
            'form': form
        }
        return render(request, 'users/register.html', context)

    def post(self, request):
        form= UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You are successfully registered, you can now login!')
            return redirect('login')
        context={
            'title': 'User Registration',
            'form': form
        }
        return render(request, 'users/register.html', context) 