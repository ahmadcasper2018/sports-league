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

    def get_total_points(self, strategy):
        score = 0
        if self.games_one:
            for game in self.games_one.all():
                score += strategy.process_scoring(game.score_one, game.score_two)
        for game in self.games_two.all():
            score += strategy.process_scoring(game.score_two, game.score_one)
        return score

    def __str__(self):
        return self.name
