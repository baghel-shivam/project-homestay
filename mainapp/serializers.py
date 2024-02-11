from rest_framework import serializers
from .models import Room, RoomImages,BookingDetail

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

    
class RoomImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImages
        fields = '__all__'

class BookingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model= BookingDetail
        fields= '__all__'