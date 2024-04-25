from rest_framework import serializers
from .models import MeetingRoom, MeetingBooking

class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = ['id', 'name', 'capacity']

class MeetingBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingBooking
        fields = ['id', 'meeting_room', 'start_time', 'end_time', 'person_capacity']

