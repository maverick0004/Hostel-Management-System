from django.shortcuts import render, redirect
from .forms import UserForm, RegistrationForm, LoginForm, SelectionForm
from django.http import HttpResponse, Http404
from selection.models import Student, Room, Hostel, Year, Course
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
        r_id_before = request.user.student.room_id

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
                    room = Room.objects.get(id=r_id_before)
                    room.vacant = True
                    room.save()
                except BaseException:
                    pass
            else:
                request.user.student.room_allotted = False
                try:
                    room = Room.objects.get(id=r_id_before)
                    room.vacant = True
                    room.save()
                except BaseException:
                    pass
            form.save()
            return render(request, 'profile.html')
    else:
        form = SelectionForm(instance=request.user.student)
        gen = request.user.student.gender
        year = request.user.student.current_year_id
        student_course = request.user.student.course_id
        hostel = Hostel.objects.filter(
            gender=gen, course=student_course, current_year=year)
        x = Room.objects.none()
        for i in range(len(hostel)):
            h_id = hostel[i].id
            if year <= 2:
                a = Room.objects.filter(
                    hostel_id=h_id, room_type='D', vacant=True)
                x = x | a
            else:
                a = Room.objects.filter(
                    hostel_id=h_id, room_type='D', vacant=True)
                x = x | a
        form.fields["room"].queryset = x
        return render(request, 'edit.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


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
