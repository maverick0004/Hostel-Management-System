from django.contrib import admin
from django.urls import path
from selection import views
from django.conf.urls import url 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='register'),
    path('reg_form/',views.register,name='reg_form'),
    path('login/',views.user_login,name='login'),
    path('hostels/<slug:hostel_name>/', views.hostel_detail_view,name='hostel'),
    path('login/edit/',views.edit,name='edit'),
    path('logout/',views.logout_view,name='logout'),
]