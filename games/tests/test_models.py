from django.test import TestCase

from games.models import Game, Team
from games.rank_utils import DefaultRankStrategy, GameCountRankStrategy
from games.score_utils import CustomScoreStrategy, DefaultScoreStrategy


class TestGameModel(TestCase):
    def setUp(self):
        self.team_1 = Team.objects.create(name="Team 1")
        self.team_2 = Team.objects.create(name="Team 2")
        self.game_1 = Game.objects.create(
            team_one=self.team_1, score_one=3, team_two=self.team_2, score_two=2
        )

    def tearDown(self):
        Team.objects.all().delete()

    def test_create_game_with_valid_inputs(self):
        self.assertEqual(str(self.game_1), "Team 1 <-X-> Team 2")

    def test_create_game_with_invalid_inputs(self):
        with self.assertRaises(Exception):
            Game.objects.create(
                team_one=4, score_one=self.team_2, team_two=3, score_two=2
            )

    def test_retrieve_team_one_name_from_game(self):
        self.assertEqual(self.game_1.team_one.name, "Team 1")

    def test_retrieve_team_two_name_from_game(self):
        self.assertEqual(self.game_1.team_two.name, "Team 2")

    def test_update_scores_of_game(self):
        self.game_1.score_one = 4
        self.game_1.score_two = 1
        self.game_1.save()
        self.game_1.refresh_from_db()
        self.assertEqual(self.game_1.score_one + self.game_1.score_two, 5)

    def test_delete_game(self):
        game = Game.objects.create(
            team_one=self.team_1, score_one=3, team_two=self.team_2, score_two=2
        )
        game_pk = game.pk
        game.delete()
        self.assertFalse(Game.objects.filter(pk=game_pk).exists())

    def test_related_name_for_team_one(self):
        game = Game.objects.create(
            team_one=self.team_1, score_one=3, team_two=self.team_2, score_two=2
        )
        games = self.team_1.games_one.all()
        self.assertIn(game, games)

    def test_related_name_for_team_two(self):
        game = Game.objects.create(
            team_one=self.team_1, score_one=3, team_two=self.team_2, score_two=2
        )
        games = self.team_2.games_two.all()
        self.assertIn(game, games)

    def test_update_team1_name(self):
        self.team_1.name = "Updated Team 1"
        self.team_1.save()
        self.game_1.refresh_from_db()
        self.assertEqual(self.game_1.team_one.name, "Updated Team 1")

    def test_update_team2_name(self):
        self.team_2.name = "Updated Team 2"
        self.team_2.save()
        self.game_1.refresh_from_db()
        self.assertEqual(self.game_1.team_two.name, "Updated Team 2")


class TestTeamModel(TestCase):
    def setUp(self):
        self.team_one = Team.objects.create(name="Team One")
        self.team_two = Team.objects.create(name="Team Two")
        self.game_one = Game.objects.create(
            team_one=self.team_one, team_two=self.team_two, score_one=10, score_two=3
        )
        self.game_two = Game.objects.create(
            team_one=self.team_one, team_two=self.team_two, score_one=3, score_two=1
        )

    def tearDown(self):
        self.team_one.delete()
        self.team_two.delete()

    def test_create_team(self):
        self.assertEqual(self.team_one.name, "Team One")

    def test_update_team_name(self):
        self.team_one.name = "Updated Team"
        self.team_one.save()
        self.team_one.refresh_from_db()
        self.assertEqual(self.team_one.name, "Updated Team")

    def test_team_one_games_count(self):
        self.assertEqual(self.team_one.games_one.count(), 2)

    def test_team_two_games_count(self):
        self.assertEqual(self.team_two.games_two.count(), 2)

    def test_team_one_points_with_default_score_strategy_case_one(self):
        strategy = DefaultScoreStrategy()
        Game.objects.create(
            team_one=self.team_one, team_two=self.team_two, score_one=3, score_two=3
        )
        Game.objects.create(
            team_one=self.team_one, team_two=self.team_two, score_one=0, score_two=3
        )
        self.assertEqual(self.team_one.get_total_points(strategy=strategy), 7)

    def test_team_one_points_with_default_score_strategy_case_two(self):
        strategy = DefaultScoreStrategy()
        self.assertEqual(self.team_one.get_total_points(strategy=strategy), 6)

    def test_team_one_points_with_default_score_strategy_case_three(self):
        self.game_one.delete()
        self.game_two.delete()
        Game.objects.create(
            team_one=self.team_one, team_two=self.team_two, score_one=3, score_two=3
        )
        self.team_one.refresh_from_db()
        strategy = DefaultScoreStrategy()
        self.assertEqual(self.team_one.get_total_points(strategy=strategy), 1)

    def test_team_one_points_with_default_score_strategy_case_four(self):
        self.game_one.delete()
        self.game_two.delete()
        Game.objects.create(
            team_one=self.team_one, team_two=self.team_two, score_one=0, score_two=3
        )
        self.team_one.refresh_from_db()
        strategy = DefaultScoreStrategy()
        self.assertEqual(self.team_one.get_total_points(strategy=strategy), 0)

    def test_team_two_points_with_default_score_strategy_case_one(self):
        strategy = DefaultScoreStrategy()
        Game.objects.create(
            team_one=self.team_one, team_two=self.team_two, score_one=3, score_two=3
        )
        Game.objects.create(
            team_one=self.team_one, team_two=self.team_two, score_one=0, score_two=3
        )
        self.assertEqual(self.team_two.get_total_points(strategy=strategy), 4)

    def test_team_two_points_with_default_score_strategy_case_two(self):
        strategy = DefaultScoreStrategy()
        self.assertEqual(self.team_two.get_total_points(strategy=strategy), 0)

    def test_team_two_points_with_default_score_strategy_case_three(self):
        self.game_one.delete()
        self.game_two.delete()
        Game.objects.create(
            team_one=self.team_one, team_two=self.team_two, score_one=3, score_two=3
        )
        self.team_one.refresh_from_db()
        strategy = DefaultScoreStrategy()
        self.assertEqual(self.team_two.get_total_points(strategy=strategy), 1)

    def test_team_two_points_with_default_score_strategy_case_four(self):
        self.game_one.delete()
        self.game_two.delete()
        Game.objects.create(
            team_one=self.team_one, team_two=self.team_two, score_one=0, score_two=3
        )
        self.team_one.refresh_from_db()
        strategy = DefaultScoreStrategy()
        self.assertEqual(self.team_two.get_total_points(strategy=strategy), 3)

    def test_team_one_points_with_custom_score_strategy_case_one(self):
        strategy = CustomScoreStrategy()
        Game.objects.create(
            team_one=self.team_one, team_two=self.team_two, score_one=3, score_two=3
        )
        Game.objects.create(
            team_one=self.team_one, team_two=self.team_two, score_one=0, score_two=3
        )
        self.assertEqual(self.team_one.get_total_points(strategy=strategy), 2)

    def test_team_two_points_with_custom_score_strategy_case_two(self):
        strategy = CustomScoreStrategy()
        self.assertEqual(self.team_two.get_total_points(strategy=strategy), 0)

    def test_team_two_points_with_custom_score_strategy_case_three(self):
        self.game_one.delete()
        self.game_two.delete()
        Game.objects.create(
            team_one=self.team_one, team_two=self.team_two, score_one=3, score_two=3
        )
        self.team_one.refresh_from_db()
        strategy = CustomScoreStrategy()
        self.assertEqual(self.team_two.get_total_points(strategy=strategy), 0)

    def test_team_two_points_with_custom_score_strategy_case_four(self):
        self.game_one.delete()
        self.game_two.delete()
        Game.objects.create(
            team_one=self.team_one, team_two=self.team_two, score_one=0, score_two=3
        )
        self.team_one.refresh_from_db()
        strategy = CustomScoreStrategy()
        self.assertEqual(self.team_two.get_total_points(strategy=strategy), 1)

    def test_teams_Default_rank_strategy_and_scoring(self):
        self.team_three = Team.objects.create(name="Team three")
        self.team_four = Team.objects.create(name="Team four")
        Game.objects.create(
            team_one=self.team_three, team_two=self.team_four, score_one=4, score_two=0
        )
        Game.objects.create(
            team_one=self.team_three, team_two=self.team_two, score_one=4, score_two=6
        )
        Game.objects.create(
            team_one=self.team_four, team_two=self.team_one, score_one=2, score_two=2
        )
        self.team_one.refresh_from_db()
        strategy = DefaultScoreStrategy()
        rank = DefaultRankStrategy()
        ranking_results = Team.rank_teams(rank_strategy=rank, score_strategy=strategy)
        actual_ranking = [
            {"team": team.name, "total_score": team.get_total_points(strategy)}
            for team in [self.team_one, self.team_three, self.team_two, self.team_four]
        ]
        self.assertEqual(ranking_results, actual_ranking)

    def test_teams_with_Default_rank_strategy_and_custom_scoring(self):
        self.team_three = Team.objects.create(name="Team three")
        self.team_four = Team.objects.create(name="Team four")
        Game.objects.create(
            team_one=self.team_three, team_two=self.team_four, score_one=4, score_two=0
        )
        Game.objects.create(
            team_one=self.team_three, team_two=self.team_two, score_one=4, score_two=6
        )
        Game.objects.create(
            team_one=self.team_four, team_two=self.team_one, score_one=2, score_two=2
        )
        self.team_one.refresh_from_db()
        strategy = CustomScoreStrategy()
        rank = DefaultRankStrategy()
        ranking_results = Team.rank_teams(rank_strategy=rank, score_strategy=strategy)
        actual_ranking = [
            {"team": team.name, "total_score": team.get_total_points(strategy)}
            for team in [self.team_one, self.team_three, self.team_two, self.team_four]
        ]
        self.assertEqual(ranking_results, actual_ranking)

    def test_teams_with_custom_rank_strategy_and_custom_scoring(self):
        self.team_three = Team.objects.create(name="Team three")
        self.team_four = Team.objects.create(name="Team four")
        Game.objects.create(
            team_one=self.team_three, team_two=self.team_four, score_one=4, score_two=0
        )
        Game.objects.create(
            team_one=self.team_three, team_two=self.team_two, score_one=4, score_two=6
        )
        Game.objects.create(
            team_one=self.team_four, team_two=self.team_one, score_one=2, score_two=2
        )
        self.team_one.refresh_from_db()
        strategy = CustomScoreStrategy()
        rank = GameCountRankStrategy()
        ranking_results = Team.rank_teams(rank_strategy=rank, score_strategy=strategy)
        actual_ranking = [
            {"team": team.name, "total_score": team.get_total_points(strategy)}
            for team in [self.team_one, self.team_two, self.team_three, self.team_four]
        ]
        self.assertEqual(ranking_results, actual_ranking)

    def test_delete_team(self):
        test_team = Team.objects.create(name="alpha")
        test_team.delete()
        self.assertFalse(Team.objects.filter(name="alpha").exists())
