from django.urls import path, re_path
from mainapp import views
app_name = 'mainapp'

urlpatterns = [

    # The home page
    # path('', views.home, name='home'),
    # path('roomDetails/<int:id>', views.roomDetails, name='roomDetails'),
    
    path('api/room_search',views.RoomSearchAPIView.as_view(), name='room_search'),
    path('api/room_details/<int:id>/',views.RoomDetailsAPIView.as_view(), name='api_room_details'),
    path('api/booking_request',views.BookingRequestApi.as_view(), name='api_booking_request'),


]
