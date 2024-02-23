from django.shortcuts import render
from django import template
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404
from .serializers import RoomSerializer
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from user.models import User 
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import FormView


'''

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
    template = 'room/roomDetails.html'
    context = {
        'selectedRoom':selectedRoom,
        'allImages':allImages,
        'all_comments':all_comments
    }
    return render(request,template, context)

'''

# A****************pi Work here ****************
class RoomSearchAPIView(APIView):
    def post(self, request):
        location = request.data.get('location', '')
        if not location:
            return Response('Bad Request, Location is required field', status=status.HTTP_400_BAD_REQUEST)
        checkin_date = request.data.get('checkin_date', '')
        checkout_date = request.data.get('checkout_date', '')
        available_rooms = Room.objects.filter(
            (Q(parent_address__state__iexact=location) |
             Q(parent_address__city__iexact=location) |
             Q(parent_address__area__iexact=location)),
             ~(Q(cheked_in_date__gte=checkin_date) & Q(cheked_in_date__lte=checkout_date)),
            ~(Q(cheked_out_date__gte=checkin_date) & Q(cheked_out_date__lte=checkout_date)),
            is_checked_in=False,
            
        )
        

        serializer = RoomSerializer(available_rooms, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RoomDetailsAPIView(APIView):
    # @login_required(login_url="/login/")
    def get(self, request, id):
        if not id:
            return Response('Bad Request, ID is required', status=status.HTTP_400_BAD_REQUEST)
        selected_room = get_object_or_404(Room, id=id)
        serializer = RoomSerializer(selected_room)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def handle_exception(self, exc):
        if isinstance(exc, Http404):
            return Response(f'Bad Request, No room found with the given id', status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)


class BookingRequestApi(APIView):
    def post(self, request):
        parentroom_id = request.data.get('parent_room', '')
        parent_user_id = request.data.get('user_id', '')
        customer_name = request.data.get('customer_name', '')
        booking_price = request.data.get('booking_price', None)
        checked_in_date = request.data.get('check_in_date', '')
        checked_out_date = request.data.get('check_out_date', '')
        if checked_in_date:
            checked_in_date = datetime(2024, 2, 11, 12, 0, 0).isoformat()
        if checked_out_date:
            checked_out_date = datetime(2024, 2, 13, 12, 0, 0).isoformat()
        request_location = request.data.get('request_location', '')
        customer_phn = request.data.get('customer_phn', '')
        customer_email = request.data.get('customer_email', '')

        if not parentroom_id or not customer_name or not customer_phn or not checked_in_date or not checked_out_date:
            return Response('Bad Request, required fields are missing', status=status.HTTP_400_BAD_REQUEST)
        
        try:
            parent_user = User.objects.get(id=parent_user_id)
        except User.DoesNotExist:
            return Response('Bad Request, user not found', status=status.HTTP_400_BAD_REQUEST)

        obj = BookingDetail()
        obj.parent_room_id = int(parentroom_id)
        obj.parent_user = parent_user
        obj.customer_name = customer_name
        obj.booking_price = booking_price
        

        obj.cheked_in_date = checked_in_date
        obj.cheked_out_date = checked_out_date
        obj.location = request_location
        obj.customer_phn = customer_phn
        if customer_email:
            obj.customer_email = customer_email
        
        obj.save()
        return Response('Booking request created successfully', status=status.HTTP_201_CREATED)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class CustomCreateSuperuserView(FormView):
    template_name = 'createsuperuser.html'
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        self.save_user(form)
        return HttpResponse('User created')
        # return super().form_valid(form)

    def save_user(self, form):
        user = form.save(commit=False)
        user.is_staff = True
        user.is_superuser = True
        user.save()
