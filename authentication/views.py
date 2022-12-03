from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from django.views import View
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate, login , logout
from userpreferences.models import UserPreferences

# from validate_email import validate_email

# Create your views here.

class UsernameValidate(View):
    def post(self,request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should be alphanumeric only'},status = 400)
        if User.objects.filter(username = username).exists():
            return JsonResponse({'username_error': 'Username already taken!'},status = 409)
        return JsonResponse({'username_valid':True})

class RegistrationView(View):
    def get(self,request):
        
        return render(request, 'authentication/register.html')

    def post(self,request):   
        if request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

            context = {"uname":username, "mail":email}

            if not User.objects.filter(username = username).exists():
                if not User.objects.filter(email = email).exists():
                    if len(password)<7:
                        messages.error(request, "Password too short")
                        return render(request, 'authentication/register.html', context)

                    user = User.objects.create_user(username = username, email = email)
                    user.set_password(password)
                    # user.is_active = False
                    user.save()
                    user_preferences = UserPreferences.objects.create(user = user, currency = "None")
                    user_preferences.save()
                    email_subject = "Activate your account"
                    email_body = 'Testing'
                    email = EmailMessage(
                        email_subject,
                        email_body,
                        'from@example.com',
                        [email],
                    )

                    # email.send(fail_silently=False)

                    messages.success(request, "Account created successfully")
                    return render(request, 'authentication/login.html')
                else:
                    messages.error(request, "Email already used")
                    return render(request, 'authentication/register.html', context)
            else:
                messages.error(request, "Username already taken")
                return render(request, 'authentication/register.html', context)

        return render(request, 'authentication/register.html')

class LoginView(View):
    def get(self,request):
        return render(request, 'authentication/login.html')

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = authenticate(username = username, password = password)
            print("User is: ", user)
            if user:
                login(request,user)
                messages.success(request, 'Welcome ' + username + ' you are now logged in')
                return redirect('expenses')
            
            messages.error(request,'Invalid Credentails! try again')
            return render(request, 'authentication/login.html')

        messages.error(request,"Please fill all fields")
        return render(request, 'authentication/login.html')


class LogoutView(View):
    def post(self,request):
        logout(request)
        return redirect('login')
