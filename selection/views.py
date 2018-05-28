from django.shortcuts import render,redirect
from .forms import UserForm,RegistrationForm,LoginForm
from django.http import HttpResponse,Http404
from selection.models import Student, Room, Hostel
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'home.html')

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            Student.objects.create(user=new_user)
            return redirect('/')
    else:
        form = UserForm()
        args = {'form':form}
        return render(request,'reg_form.html',args)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,username=cd['username'],password=cd['password'])
            if user is not None :
                if user.is_active:
                    login(request,user)
                    #return HttpResponse('Authenticated Succesfully')
                    return render(request,'profile.html')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
        return render(request,'login.html',{'form':form})

@login_required
def edit(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST,instance=request.user.student)
        if form.is_valid():
            form.save()
            return render(request,'profile.html')
    else:
        form = RegistrationForm(instance=request.user.student)
        return render(request,'edit.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('/')

def hostel_detail_view(request, hostel_name):
    try:
        this_hostel = Hostel.objects.get(name=hostel_name)
    except Hostel.DoesNotExist:
        raise Http404("Invalid Hostel Name")
    context = {'hostel': this_hostel, 'rooms': Room.objects.filter(hostel=this_hostel)}
    return render(request, 'hostels.html', context)
