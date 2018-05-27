from django.shortcuts import render
from django.http import Http404
from selection.models import Room, Hostel


# Create your views here.
def hostel_detail_view(request, hostel_name):
    try:
        this_hostel = Hostel.objects.get(name=hostel_name)
    except Hostel.DoesNotExist:
        raise Http404("Invalid Hostel Name")
    context = {'hostel': this_hostel, 'rooms': Room.objects.filter(hostel=this_hostel)}
    return render(request, 'hostels.html', context)
