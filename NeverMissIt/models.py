from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# model for the created events taking the User "id" as the foreign key
class EventDetails(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Event Title')
    createduserid = models.ForeignKey(User, on_delete=models.CASCADE) #the foreign key to the User
    description = models.TextField(verbose_name='Event Description')
    eventdate = models.DateField(verbose_name='Event Date')
    location = models.CharField(max_length=200, verbose_name='Event Happening At')
    lastdatetoreg = models.DateField(verbose_name='Registration Deadline')
    maxparticipants = models.PositiveIntegerField(verbose_name='Max. Participants')

    def __str__(self):
        return self.title  # to show the tile of the event when accessing it as object

# model for the participant list of events using foreign key "id" from EventDetails for the event recognition and "id" from User for the team leader recognition
class EventParticipants(models.Model):
    eventid = models.ForeignKey(EventDetails, on_delete=models.CASCADE) # foreign key to the EventDetails for event recognition
    teamleader = models.ForeignKey(User, on_delete=models.CASCADE) # foreign key to the User to set the team leader as the registering user as default
    participants = models.TextField() # storing the participants names and is planned to be stored as a single string seperated by special symbol. not going to create form form this model.
    # the foreign key from User is under observation and can change if needed .

    def __str__(self):
        return self.eventid.title + " (" + self.teamleader.username + ")"