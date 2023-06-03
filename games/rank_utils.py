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
        annotated_list = []
        for team in queryset:
            total_score = team.get_total_points(score_strategy)
            games_count = team.get_games_count
            annotated_team = {
                "team": team.name,
                "total_score": total_score,
                "games": games_count,
            }
            annotated_list.append(annotated_team)

        sorted_list = sorted(
            annotated_list,
            key=lambda item: (item["total_score"], item["games"]),
            reverse=True,
        )

        # Create a new list without the "games" key
        results = []
        for item in sorted_list:
            item_without_games = {k: v for k, v in item.items() if k != "games"}
            results.append(item_without_games)

        return results
