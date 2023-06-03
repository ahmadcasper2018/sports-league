from rest_framework import serializers

from games.models import Game, Team


class GameSerializer(serializers.ModelSerializer):
    team_one = serializers.CharField(source="team_one.name")
    team_two = serializers.CharField(source="team_two.name")

    class Meta:
        model = Game
        fields = (
            "id",
            "team_one",
            "score_one",
            "team_two",
            "score_two",
        )

    def create(self, validated_data):
        team_one_data = validated_data.pop("team_one")
        team_two_data = validated_data.pop("team_two")

        team_one, _ = Team.objects.get_or_create(**team_one_data)
        team_two, _ = Team.objects.get_or_create(**team_two_data)

        validated_data["team_one"] = team_one
        validated_data["team_two"] = team_two

        return super().create(validated_data)

    def update(self, instance, validated_data):
        team_one_data = validated_data.pop("team_one", None)
        team_two_data = validated_data.pop("team_two", None)

        if team_one_data:
            team_one, _ = Team.objects.get_or_create(**team_one_data)
            instance.team_one = team_one

        if team_two_data:
            team_two, _ = Team.objects.get_or_create(**team_two_data)
            instance.team_two = team_two

        return super().update(instance, validated_data)
