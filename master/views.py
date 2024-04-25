
# views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import MeetingRoom, MeetingBooking
from .serializers import MeetingRoomSerializer, MeetingBookingSerializer

class ListAvailableRooms(APIView):
    def get(self, request):
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        
        if start_time is None or end_time is None:
            return Response({'error': 'start_time and end_time parameters are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        available_rooms = MeetingRoom.objects.exclude(meetingbooking__start_time__lt=start_time, meetingbooking__end_time__gt=end_time).order_by('capacity')
        serializer = MeetingRoomSerializer(available_rooms, many=True)
        return Response(serializer.data)

class BookMeeting(APIView):
    def post(self, request):
        serializer = MeetingBookingSerializer(data=request.data)
        if serializer.is_valid():
            meeting_room_id = serializer.validated_data['meeting_room']
            start_time = serializer.validated_data['start_time']
            end_time = serializer.validated_data['end_time']
            person_capacity = serializer.validated_data['person_capacity']
            
            # time overlaps with buffer time
            buffer_times = [
                ('09:00', '09:15'),
                ('13:15', '13:45'),
                ('18:45', '19:00')
            ]
            for buffer_start, buffer_end in buffer_times:
                if start_time.time() < buffer_end and end_time.time() > buffer_start:  # Agar hum start time ko end time ke saath compare karenge, toh hum dekhenge ki booking request ki end time buffer time se pehle hai ya nahi. Aur agar hum end time ko start time ke saath compare karenge, toh hum dekhenge ki booking request ki start time buffer time ke baad hai ya nahi.
                    return Response({'error': 'Booking cannot overlap with buffer time'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if person capacity is within the range
            if person_capacity < 2 or person_capacity > 20:
                return Response({'error': 'Person capacity should be between 2 and 20'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Find the most suitable room based on capacity
            suitable_rooms = MeetingRoom.objects.filter(capacity__gte=person_capacity)
            if suitable_rooms.exists():
                suitable_room = suitable_rooms.order_by('capacity').first()
                booking = serializer.save(meeting_room=suitable_room)
                return Response(MeetingBookingSerializer(booking).data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'No vacant room available for the specified capacity'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)