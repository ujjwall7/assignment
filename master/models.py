from django.db import models
from django.utils import timezone

class MeetingRoom(models.Model):
    name = models.CharField(max_length=50, unique=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

# Meeting booking model
class MeetingBooking(models.Model):
    meeting_room = models.ForeignKey(MeetingRoom, on_delete=models.CASCADE, related_name='meeting_room')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)
    person_capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.meeting_room} - {self.start_time.strftime('%Y-%m-%d %H:%M')} to {self.end_time.strftime('%Y-%m-%d %H:%M')}"







