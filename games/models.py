# Create your models here.
from django.db import models


class Game(models.Model):
    team_one = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="games_one"
    )
    score_one = models.PositiveIntegerField()
    team_two = models.ForeignKey(
        "Team", on_delete=models.CASCADE, related_name="games_two"
    )
    score_two = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.team_one.name} <-X-> {self.team_two.name}"


class Team(models.Model):
    name = models.CharField(unique=True, max_length=32)

    @property
    def get_games_count(self):
        return self.games_one.count() + self.games_two.count()

    def __str__(self):
        return self.name
