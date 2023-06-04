import os

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from games.api.serializers import GameSerializer
from games.models import Game, Team

User = get_user_model()


class GameRecordsUploadTestCase(APITestCase):
    def test_upload_games_csv(self):
        # Create a test CSV file
        self.user = User.objects.create(username="user", password="password")
        self.client = APIClient()
        self.token = AccessToken.for_user(self.user)
        self.auth_header = "Bearer {}".format(self.token)
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)

        csv_data = "Team AA,3,Team BB,1\n"
        csv_data += "Team CC,2,Team DD,2\n"

        csv_file = open("test.csv", "w")
        csv_file.write(csv_data)
        csv_file.close()

        team_a = Team.objects.create(name="Team AA")
        team_b = Team.objects.create(name="Team BB")
        team_c = Team.objects.create(name="Team CC")
        team_d = Team.objects.create(name="Team DD")

        url = f"{reverse('game-list')}upload-games-csv/"

        with open("test.csv", "rb") as file:
            data = {"csv_file": file}
            response = self.client.post(url, data, format="multipart")

        os.remove("test.csv")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Game.objects.count(), 2)

        # Assert the created game objects
        game1 = Game.objects.get(
            team_one=team_a, score_one=3, team_two=team_b, score_two=1
        )
        game2 = Game.objects.get(
            team_one=team_c, score_one=2, team_two=team_d, score_two=2
        )

        self.assertIsNotNone(game1)
        self.assertIsNotNone(game2)


class GameAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="user", password="password")
        self.team_a = Team.objects.create(name="Team A")
        self.team_b = Team.objects.create(name="Team B")

        self.game1 = Game.objects.create(
            team_one=self.team_a, score_one=3, team_two=self.team_b, score_two=1
        )
        self.game2 = Game.objects.create(
            team_one=self.team_b, score_one=2, team_two=self.team_a, score_two=2
        )
        self.client = APIClient()
        self.token = AccessToken.for_user(self.user)
        self.auth_header = "Bearer {}".format(self.token)
        self.client.credentials(HTTP_AUTHORIZATION=self.auth_header)

    def test_create_game(self):
        url = reverse("game-list")
        data = {
            "team_one": "Real Madrid",
            "score_one": 2,
            "team_two": "Barcelona",
            "score_two": 1,
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        game = Game.objects.latest("id")
        serializer = GameSerializer(game)

        self.assertEqual(response.data, serializer.data)

    def test_retrieve_game(self):
        url = reverse("game-detail", args=[self.game1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = GameSerializer(self.game1)
        self.assertEqual(response.data, serializer.data)

    def test_update_game(self):
        url = reverse("game-detail", args=[self.game1.id])
        data = {
            "team_one": "Team X",
            "score_one": 4,
            "team_two": "Team D",
            "score_two": 2,
        }

        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        game = Game.objects.get(id=self.game1.id)
        serializer = GameSerializer(game)

        self.assertEqual(response.data, serializer.data)

    def test_delete_game(self):
        url = reverse("game-detail", args=[self.game1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Game.objects.filter(id=self.game1.id).exists())
