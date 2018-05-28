from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User,default=None,null=True,on_delete=models.CASCADE)
    gender_choices = [('M','Male'),('F','Female')]
    student_name = models.CharField(max_length=200,null=True)
    father_name = models.CharField(max_length=200,null=True)
    enrollment_no = models.CharField(max_length=10,unique=True,null=True)
    current_sem = models.IntegerField(default=None,null=True)
    dob = models.DateField(max_length=10,help_text="format : YYYY-MM-DD",null=True)
    gender = models.CharField(choices=gender_choices,max_length=1,default=None,null=True)
    room = models.OneToOneField('Room',blank=True,on_delete=models.CASCADE,null=True)
    room_allotted = models.BooleanField(default=False)

    '''def __str__(self):
            return self.student_name'''
            
class Room(models.Model):
    r_type = [('S','Single Occupancy'),('D','Double Occupancy')]
    no = models.CharField(max_length=5)
    name = models.CharField(max_length=10)
    room_type = models.CharField(choices=r_type,max_length=1,default=None)
    vacant = models.BooleanField(default=False)
    hostel = models.ForeignKey('Hostel',on_delete=models.CASCADE)

    def __str__(self):
        return self.no

class Hostel(models.Model):
    name = models.CharField(max_length=5)    
    warden = models.CharField(max_length=100,blank=True)
    caretaker = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.name

