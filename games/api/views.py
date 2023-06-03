import csv

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from games.api.serializers import GameSerializer
from games.models import Game, Team


class GameViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @action(methods=["post"], detail=False, url_path="upload-games-csv")
    def upload_games_csv(self, request):
        csv_file = request.data.get("csv_file")
        decoded_file = csv_file.read().decode("utf-8")
        reader = csv.reader(decoded_file.splitlines())
        data = list(reader)
        for row in data:
            Game.objects.create(
                team_one=Team.objects.get_or_create(name=row[0])[0],
                score_one=row[1],
                team_two=Team.objects.get_or_create(name=row[2])[0],
                score_two=row[3],
            )
        return Response(status=status.HTTP_200_OK)
