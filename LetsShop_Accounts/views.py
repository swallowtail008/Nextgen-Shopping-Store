from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import uuid
from django.conf import settings
from .models import *
from django.core.mail import send_mail

###User login and logout
#------------------------------------------------------------------------------
def LOGIN(request):
    if request.method =='POST':
        UserName=request.POST.get('username')
        Pass=request.POST.get('password')
        if len(Pass) == 0:
            messages.warning(request, "No Password Found.")
            return redirect('login')

        user = authenticate(username= UserName, password=Pass)
        if user:
            prof = Profile.objects.get(user = user)
            if prof.is_verified == True:
               login(request, user)
               return redirect('user_desh')
            else:
              return redirect('error')
            
        else:
            messages.warning(request,"Username or Password Not Found")
    return render(request,'Accounts/login.html')

def LOGOUT(request):
    logout(request)
    messages.warning(request,"You are logged Out")
    return redirect('login')

#--------------------------------------------------------------------------------------------

### User email verfied reg

#----------------------------------------------------------------------------------------------
def REG(request):
    if request.method =='POST':
        First_name=request.POST.get('first')
        Last_name=request.POST.get('last')
        UserName=request.POST.get('name')
        Email=request.POST.get('email')
        # Check if email is a Gmail address
        if not Email.endswith('@gmail.com'):
            messages.warning(request, "Please use a valid Gmail address for registration.")
            return redirect('reg')
        Pass=request.POST.get('pass')
        Pass1=request.POST.get('pass1')
        if UserName is not None:
            for i in UserName:
                if i in ['.','@','/','*','$']:
                    messages.warning(request, "Your Username has special character, please remove them.")
                    return redirect('reg')

            if User.objects.filter(username=UserName).exists():
                messages.warning(request, "Your Username already taken! Try New.")
            elif User.objects.filter(email=Email).exists():
                messages.warning(request, "Your Email already taken! Try New.")
            else:
                if Pass == Pass1:
                   user = User.objects.create_user(first_name=First_name,last_name=Last_name,username=UserName,email=Email,password=Pass)
                   user.set_password(Pass)
                   auth_token = str(uuid.uuid4())
                   pro_obj = Profile.objects.create(user = user, auth_token = auth_token)
                   pro_obj.save()
                   send_mail_registration(Email, auth_token)
                   return redirect('success')

                   return redirect('login')
                else:
                    messages.warning(request, "Your Given Password Not Matched.")

    return render(request,'Accounts/registration.html')

def success(request):
     
     return render(request,'Accounts/success.html')

def token_send(request):
     
     return render(request,'Accounts/token_send.html')

def error(request):
     
     return render(request,'Accounts/error.html')

def send_mail_registration(Email, auth_token):
    subject = 'Your Account Authentication Link'
    message = f'hi, Here is the verification link for your account: http://127.0.0.1:8000/accounts/verify/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)


def verify(request, auth_token):
    profile_obj= Profile.objects.filter(auth_token=auth_token).first()
    profile_obj.is_verified= True
    profile_obj.save()
    messages.success(request,'Congratulation Account Verify its done')
    return redirect('login')
#------------------------------------------------------------------------------------------------

#### pass reset####
#------------------------------------------------------------------------------------------------
def RESET_PASS(request):
     if request.method =='POST':
        email=request.POST.get('email')
        if email:
            user_prof = User.objects.filter(email=email)
            if user_prof:
                res_prof= Profile.objects.get(user = user_prof)
                auth_token = res_prof.auth_token 
                send_mail_reset(email, auth_token)
                return redirect('success1')
            else:
                messages.warning(request,"Mail Address Not Found")
                return redirect('reset')
        

     return render(request,'Accounts/reset_pass.html')

def success1(request):
     return render(request,'Accounts/success1.html')

def send_mail_reset(Email, auth_token):
    subject = 'Your Account Password Reset Link'
    message = f'hi, Here is the Password Reset link for your account Pass Reset: http://127.0.0.1:8000/accounts/Reset_user_pass/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [Email]
    send_mail(subject, message, email_from, recipient_list)

def Reset_user_pass(request, auth_token):
    profile_obj= Profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if request.method == 'POST':
            pass0 = request.POST.get('pass')
            pass1 = request.POST.get('pass1')
            if pass0 == pass1:
                user = profile_obj.user
                user.set_password(pass0)
                user.save()
                messages.success(request, "Your Password Successfully Changed.")
                return redirect('login')
            else:
                messages.success(request, "Your Password and Retype Password Not Matched.")

    return render(request, 'Accounts/new_pass.html')

#-------------------------------------------------------------------------------------------------------------------------
#User Dashboard
#-------------------------------------------------------------------------------------------------------------------------

def user_desh(request):
    user = request.user
    add = Address.objects.filter(user=user)
    return render(request,'Accounts/User-desh.html', locals())

