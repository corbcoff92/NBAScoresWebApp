from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    '''
    Model representing an NBA Team
    '''
    team_name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=30)
    abbreviation = models.CharField(max_length=3)
    team_id = models.IntegerField(primary_key=True)

    def __str__(self):
        '''
        Display the team's name for print statements.
        '''
        return self.team_name


class HiddenGamePreferences(models.Model):
    '''
    Model representing the hidden score preferences for a specific user.
    '''
    user = models.OneToOneField(
        User, related_name="preferences", on_delete=models.CASCADE)
    hide_scores = models.BooleanField(default=False)
    hide_after_period = models.IntegerField(default=4)
    minutes_remaining = models.IntegerField(default=12)
    max_score_difference = models.IntegerField(default=0)

    def __str__(self):
        '''
        Display the user's username for print statements.
        '''
        return self.user.username
