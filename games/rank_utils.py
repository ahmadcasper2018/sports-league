class RankStrategy:
    def process_ranking(self, queryset, score_strategy=None):
        raise NotImplementedError("Subclasses must implement process_ranking()")


class DefaultRankStrategy(RankStrategy):
    def process_ranking(self, queryset, score_strategy=None):
        annotated_list = []
        for team in queryset:
            total_score = team.get_total_points(score_strategy)
            annotated_team = {"team": team.name, "total_score": total_score}
            annotated_list.append(annotated_team)

        return sorted(
            annotated_list,
            key=lambda item: (item["total_score"], item["team"]),
            reverse=True,
        )


class GameCountRankStrategy(RankStrategy):
    def process_ranking(self, queryset, score_strategy=None):
        # Sort the teams based on their total points and number of games
        return sorted(
            queryset,
            key=lambda team: (
                team.get_total_points(score_strategy),
                team.get_games_count(),
            ),
            reverse=True,
        )
