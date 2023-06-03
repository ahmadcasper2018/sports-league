class ScoreStrategy:
    def process_scoring(self, score_one, score_two):
        raise NotImplementedError("Subclasses must implement process_payment()")


class DefaultScoreStrategy(ScoreStrategy):
    def process_scoring(self, score_one, score_two):
        if score_one > score_two:
            return 3
        elif score_one == score_two:
            return 1
        return 0


class CustomScoreStrategy(ScoreStrategy):
    def process_scoring(self, score_one, score_two):
        # Implement your custom scoring algorithm here
        if score_one > score_two:
            return 1
        elif score_one == score_two:
            return 0
        return 0
