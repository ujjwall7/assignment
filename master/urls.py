from django.urls import path
from .views import ListAvailableRooms, BookMeeting

urlpatterns = [
    path('available-rooms/', ListAvailableRooms.as_view(), name='list_available_rooms'),
    path('book-meeting/', BookMeeting.as_view(), name='book_meeting'),
]
