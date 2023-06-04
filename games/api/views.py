import csv

from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from games.api.serializers import GameSerializer
from games.models import Game, Team
from games.strategies_tracker import get_available_strategies


class GameViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (IsAuthenticated,)

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

    @action(methods=["get"], detail=False)
    def rank(self, request):
        active_score_strategies = get_available_strategies("score")
        active_rank_strategies = get_available_strategies("rank")
        scoring_method = (
            self.request.query_params.get("score_strategy") or "DefaultScoreStrategy"
        )
        rank_method = (
            self.request.query_params.get("rank_strategy") or "DefaultRankStrategy"
        )
        ranking_result = Team.rank_teams(
            rank_strategy=active_rank_strategies.get(rank_method)(),
            score_strategy=active_score_strategies.get(scoring_method)(),
        )

        return JsonResponse(ranking_result, safe=False)

    @action(methods=["get"], detail=False, url_path="score-strategies")
    def score_strategies(self, request):
        strategies = list(get_available_strategies("score").keys())
        data = {"strategies": strategies}
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False, url_path="rank-strategies")
    def rank_strategies(self, request):
        strategies = list(get_available_strategies("rank").keys())
        data = {"strategies": strategies}
        return Response(data, status=status.HTTP_200_OK)
