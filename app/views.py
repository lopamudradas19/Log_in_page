from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from app.forms import *
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def Registration(request):
    usfo=UserForm()
    pfo=ProfileForm()
    d={'usfo':usfo,'pfo':pfo}
    if request.method=='POST' and request.FILES:
        usfd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if usfd.is_valid() and pfd.is_valid():
            NSUFO=usfd.save(commit=False)
            submittedpassword=usfd.cleaned_data['password']
            NSUFO.set_password(submittedpassword)
            NSUFO.save()
            
            NSPO=pfd.save(commit=False)
            NSPO.username=NSUFO
            NSPO.save()
            
            send_mail('Registration',
                    'Your Registration is Successfull',
                    'lopamudradas19012001@gmail.com',
                      recipient_list=[NSUFO.email],
                      fail_silently=False
                          )

            return HttpResponse('entered data is submitted')
        
    return render(request,'registration.html',d)


def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)

    return render(request,'home.html')


def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO:
            if AUO.is_active:
                login(request,AUO)
                request.session['username']=username
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('Not a Active User')
        else:
            return HttpResponse('Invalid Details')
    return render(request,'user_login.html')



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display_details(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_details.html',d)

@login_required
def change_password(request):
    if request.method=='POST':
        PW=request.POST['PW']
        username=request.session['username']
        UO=User.objects.get(username=username)
        UO.set_password(PW)
        UO.save()
        return HttpResponse('password changed sucessfully')
    return render(request,'change_password.html')


def reset_password(request):
    if request.method=='POST':
        UN=request.POST['UN']
        PW=request.POST['PW']
        LUO=User.objects.filter(username=UN)
        if LUO:
            UO=LUO[0]
            UO.set_password(PW)
            UO.save()
            return HttpResponse('password reset is done')
        else:
            return HttpResponse('invalid username')
    return render(request,'reset_password.html')

    

