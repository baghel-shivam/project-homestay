from django.urls import path, re_path
from mainapp import views
app_name = 'mainapp'

urlpatterns = [
    
    path('api/room_search',views.RoomSearchAPIView.as_view(), name='room_search'),
    path('api/room_details/<int:id>/',views.RoomDetailsAPIView.as_view(), name='api_room_details'),
    path('api/booking_request',views.BookingRequestApi.as_view(), name='api_booking_request'),
    path('api/add_new_property',views.AddNewProperty.as_view(), name='add_new_property'),
    # path('createsuperuser_9090/', views.CustomCreateSuperuserView.as_view(), name='custom_createsuperuser'),


]
