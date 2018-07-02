from django.shortcuts import render, redirect
from .forms import UserForm, RegistrationForm, LoginForm, SelectionForm
from django.http import HttpResponse, Http404
from selection.models import Student, Room, Hostel
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            Student.objects.create(user=new_user)
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password1'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('login/edit/')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = UserForm()
        args = {'form': form}
        return render(request, 'reg_form.html', args)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'profile.html')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


@login_required
def edit(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance=request.user.student)
        if form.is_valid():
            form.save()
            return render(request, 'profile.html')
    else:
        form = RegistrationForm(instance=request.user.student)
        return render(request, 'edit.html', {'form': form})


@login_required
def select(request):
    if request.user.student.room:
        room_id_old = request.user.student.room_id

    if request.method == 'POST':
        form = SelectionForm(request.POST, instance=request.user.student)
        if form.is_valid():
            if request.user.student.room_id:
                request.user.student.room_allotted = True
                r_id_after = request.user.student.room_id
                room = Room.objects.get(id=r_id_after)
                room.vacant = False
                room.save()
                try:
                    room = Room.objects.get(id=room_id_old)
                    room.vacant = True
                    room.save()
                except BaseException:
                    pass
            else:
                request.user.student.room_allotted = False
                try:
                    room = Room.objects.get(id=room_id_old)
                    room.vacant = True
                    room.save()
                except BaseException:
                    pass
            form.save()
            return render(request, 'profile.html')
    else:
        form = SelectionForm(instance=request.user.student)
        student_gender = request.user.student.gender
        student_course = request.user.student.course
        student_room_type = request.user.student.course.room_type
        hostel = Hostel.objects.filter(
            gender=student_gender, course=student_course)
        x = Room.objects.none()
        if student_room_type == 'B':
            for i in range(len(hostel)):
                h_id = hostel[i].id
                a = Room.objects.filter(
                    hostel_id=h_id, room_type=['A', 'B'], vacant=True)
                x = x | a
        else :
            for i in range(len(hostel)):
                h_id = hostel[i].id
                a = Room.objects.filter(
                    hostel_id=h_id, room_type=student_room_type, vacant=True)
                x = x | a
        form.fields["room"].queryset = x
        return render(request, 'select_room.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')

def BH5_Floor1(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms':room_list}
    return render(request, 'BH5_Floor1.html',context=room_dict)

def BH5_Floor2(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms':room_list}
    return render(request, 'BH5_Floor2.html',context=room_dict)

def BH5_Floor3(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms':room_list}
    return render(request, 'BH5_Floor3.html',context=room_dict)

def BH5_Floor4(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms':room_list}
    return render(request, 'BH5_Floor4.html',context=room_dict)

def BH5_Floor5(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms':room_list}
    return render(request, 'BH5_Floor5.html',context=room_dict)

def BH5_Floor6(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms':room_list}
    return render(request, 'BH5_Floor6.html',context=room_dict)

def BH5_GroundFloor(request):
    room_list = Room.objects.order_by('name')
    room_dict = {'rooms':room_list}
    return render(request, 'BH5_GroundFloor.html',context=room_dict)



def hostel_detail_view(request, hostel_name):
    try:
        this_hostel = Hostel.objects.get(name=hostel_name)
    except Hostel.DoesNotExist:
        raise Http404("Invalid Hostel Name")
    context = {
        'hostel': this_hostel,
        'rooms': Room.objects.filter(
            hostel=this_hostel)}
    return render(request, 'hostels.html', context)
