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


# ****************Api Work here ****************
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
             Q(site_name__icontains=location) |
             Q(parent_address__pincode__iexact=location) |
             Q(parent_address__area__iexact=location)),
             ~(Q(cheked_in_date__gte=checkin_date) & Q(cheked_in_date__lte=checkout_date)),
            ~(Q(cheked_out_date__gte=checkin_date) & Q(cheked_out_date__lte=checkout_date)),
            is_checked_in=False,is_room_approved_for_listing=True
        )
        data_array = []
        for room_data in available_rooms:
            serialized_data = RoomSerializer(room_data)
            data_dict = serialized_data.data
            data_dict['img_array'] = room_data.rooms_images.all().order_by('order').values('order','image_field')
            data_array.append(data_dict)
        return Response(data_array, status=status.HTTP_200_OK)

class RoomDetailsAPIView(APIView):
    def get(self, request, id):
        if not id:
            return Response('Bad Request, ID is required', status=status.HTTP_400_BAD_REQUEST)
        selected_room = get_object_or_404(Room, id=id)
        serializer = RoomSerializer(selected_room)
        data = serializer.data
        data['img_array'] = selected_room.rooms_images.all().order_by('order').values('order','image_field')
        return Response(data, status=status.HTTP_200_OK)
    
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
        except:
            parent_user = False
        try:
            paretn_room = Room.objects.get(id=parentroom_id)
        except:
            return Response('Bad Request, Room not found', status=status.HTTP_400_BAD_REQUEST)
        obj = BookingDetail()
        obj.parent_room_id = parentroom_id
        if parent_user:
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

class AddNewProperty(APIView):
    def post(self,request):
        #Create New Address
        addressObj = Address()
        addressObj.state = request.data.get('state', '')
        addressObj.city = request.data.get('city', '')
        addressObj.area = request.data.get('area', '')
        addressObj.pincode = request.data.get('pincode', '')
        addressObj.save()

        roomObj = Room(parent_address=addressObj)
        roomObj.site_name = request.data.get('site_name', '')
        roomObj.full_addres = request.data.get('full_addres_one_line', '')
        roomObj.front_img = request.data.get('front_img', '')
        roomObj.category = request.data.get('category', '') #Choice field
        roomObj.base_price = request.data.get('base_price', '')
        roomObj.price_currency = request.data.get('price_currency', '') #Choice Field
        roomObj.is_couple_allowed = request.data.get('is_couple_allowed', '')
        roomObj.can_locals_stay = request.data.get('can_locals_stay', '')
        roomObj.should_coupon_applied = request.data.get('should_coupon_applied', '')
        roomObj.is_wifi_available = request.data.get('is_wifi_available', '')
        roomObj.is_tv_available = request.data.get('is_tv_available', '')
        roomObj.is_ac_available = request.data.get('is_ac_available', '')
        roomObj.is_parking_available = request.data.get('is_parking_available', '')
        roomObj.is_housekeeping_available = request.data.get('is_housekeeping_available', '')
        roomObj.about_this_room = request.data.get('about_this_room', '')
        roomObj.contact_person = request.data.get('contact_person', '')
        roomObj.contact_email = request.data.get('contact_email', '')
        roomObj.contact_phn = request.data.get('contact_phn', '')
        roomObj.how_to_reach = request.data.get('how_to_reach', '')
        roomObj.nearest_attraction_1 = request.data.get('nearest_attraction_1', '')
        roomObj.nearest_attraction_2 = request.data.get('nearest_attraction_2', '')
        roomObj.save()
        return Response('Site listed successfully', status=status.HTTP_201_CREATED)

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
    def save_user(self, form):
        user = form.save(commit=False)
        user.is_staff = True
        user.is_superuser = True
        user.save()
