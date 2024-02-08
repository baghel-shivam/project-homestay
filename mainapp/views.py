from django.shortcuts import render
from django import template
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *


@login_required(login_url="/login/")
def home(request):
    if request.method == 'POST':
        location = request.POST.get('location','')
        checkin_date = request.POST.get('checkin_date','')
        checkout_date = request.POST.get('checkout_date','')
        available_rooms = Room.objects.filter(Q(parent_address__state__iexact = location)|Q(parent_address__city__iexact = location)| Q(parent_address__area__iexact = location), is_checked_in=False)
        
        context = {
            'available_rooms':available_rooms,
            'location':location,
            'checkin_date':checkin_date,
            'checkout_date':checkout_date,
        }
        template = 'home/room_search_results.html'
        print(available_rooms[0].front_img.url)
        return render(request,template, context)
    template = 'home/mainHome.html'
    return render(request,template)


@login_required(login_url="/login/")
def roomDetails(request,id):
    selectedRoom = Room.objects.get(id=id)
    allImages = RoomImages.objects.filter(parent_room=selectedRoom)
    all_comments =  selectedRoom.booking_details.all().values('comment','rating','customer_name')
    print(all_comments, 'hello s')
    print(allImages, 'hello sir')
    template = 'room/roomDetails.html'
    context = {
        'selectedRoom':selectedRoom,
        'allImages':allImages,
        'all_comments':all_comments
    }
    return render(request,template, context)
