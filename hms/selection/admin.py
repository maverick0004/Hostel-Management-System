from django.contrib import admin
from .models import Student,Room,Hostel

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = ['student_name','father_name','gender','enrollment_no','dob','current_sem','room','room_alloted']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
	list_display = ['no','name','room_type','vacant','hostel']

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
	list_display = ['name','warden','caretaker']
