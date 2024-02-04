from django.urls import path, re_path
from mainapp import views
app_name = 'mainapp'

urlpatterns = [

    # The home page
    path('', views.home, name='home'),
    path('roomDetails/<int:id>', views.roomDetails, name='roomDetails'),


]
