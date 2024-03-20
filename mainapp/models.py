from django.db import models
import os
import re
from user.models import User
# Create your models here.
room_category = (('Economy','Economy'),
                ('Premium','Premium'))

currency_opt = (('INR','INR'),('US Dollar','US Dollar'))

class Address(models.Model):
    state = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    area = models.CharField(max_length=500, blank=True, null=True)
    pincode = models.IntegerField()

    def __str__(self):
        return self.city


def room_images_upload_path(instance, filename): #Path for room images
    site_name = instance.parent_room.site_name
    site_name_cleaned = re.sub(r'[^\w\-_]', '', site_name)
    return os.path.join(site_name_cleaned, 'RoomsImages', filename)

def room_front_images_upload_path(instance, filename): #Path for room images
    site_name = instance.site_name
    site_name_cleaned = re.sub(r'[^\w\-_]', '', site_name)
    return os.path.join(site_name_cleaned, 'RoomsImages', filename)

class Room(models.Model):
    parent_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='linked_rooms')
    site_name = models.CharField(max_length=500, blank=True, null=True)
    full_addres = models.CharField(max_length=1000, blank=True, null=True)
    cheked_in_date = models.DateTimeField(blank=True,null=True)
    cheked_out_date = models.DateTimeField(blank=True,null=True)
    is_checked_in = models.BooleanField(default=False)
    front_img = models.FileField(blank=True,null=True, upload_to=room_front_images_upload_path)
    category = models.CharField(max_length=100, choices= room_category, blank=True,null=True)
    base_price = models.IntegerField(blank=True, null=True)
    price_currency = models.CharField(choices=currency_opt, blank=True, null=True, max_length=50, default='INR')
    is_couple_allowed = models.BooleanField(default=False, blank=True, null=True)
    can_locals_stay = models.BooleanField(default=True, null=True, blank=True)
    should_coupon_applied = models.BooleanField(default=False, blank=True, null=True)
    is_wifi_available = models.BooleanField(default=True)
    is_tv_available = models.BooleanField(default=True)
    is_ac_available = models.BooleanField(default=True)
    is_parking_available = models.BooleanField(default=False)
    is_housekeeping_available = models.BooleanField(default=True)
    is_room_approved_for_listing = models.BooleanField(default=False)
    is_recommended= models.BooleanField(default=False)
    nearest_railway_station = models.CharField(blank=True, null=True, max_length=200)
    distance_from_rs = models.IntegerField(null=True,blank=True, verbose_name= 'Distance from nearest railway station (km)')
    nearest_metro_station = models.CharField(blank=True, null=True, max_length=200)
    distance_from_ms = models.IntegerField(null=True,blank=True, verbose_name= 'Distance from nearest metro station (km)')
    nearest_airport = models.CharField(blank=True, null=True, max_length=200)
    distance_from_ap = models.IntegerField(null=True,blank=True, verbose_name= 'Distance from nearest Air Port (km)')
    about_this_room = models.TextField(max_length=10000, blank=True, null=True)
    contact_person = models.CharField(max_length=200, blank=True, null=True)
    contact_email = models.CharField(max_length=300, blank=True, null=True)
    contact_phn = models.CharField(max_length=15, blank=True, null=True)
    how_to_reach =  models.TextField(blank=True, null=True, max_length=5000)

    def __str__(self):
        return self.site_name


class RoomImages(models.Model):
    parent_room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='rooms_images')
    order = models.IntegerField(blank=True, null=True, default=0)
    image_field = models.FileField(blank=True, null=True, upload_to= room_images_upload_path)



class BookingDetail(models.Model):
    parent_room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True,null=True,related_name='booking_details')
    parent_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True,null=True,related_name='users_booking_details')
    customer_name = models.CharField(max_length=200, blank=True, null=True)
    booking_price = models.IntegerField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    comment = models.TextField(max_length=3000, blank=True, null=True)
    is_coupon_applied = models.BooleanField(default=False, blank=True, null=True)
    cheked_in_date = models.DateTimeField(blank=True, null=True)
    cheked_out_date = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=500, blank=True,null=True)
    customer_phn = models.CharField(max_length=15, blank=True,null=True)
    customer_email = models.EmailField(blank=True,null=True)
    is_booking_approved = models.BooleanField(default=False)
    def __str__(self):
        return self.customer_name if self.customer_name else self.id

