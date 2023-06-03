import inspect

from games import rank_utils, score_utils


def get_available_strategies(strategy):
    strategy_meta = {}
    if strategy == "score":
        strategy_meta.update({"base": "ScoreStrategy", "module": score_utils})
    elif strategy == "rank":
        strategy_meta.update({"base": "RankStrategy", "module": rank_utils})
    else:
        raise ValueError("Invalid strategy: {}".format(strategy))
    members = inspect.getmembers(strategy_meta.get("module"))
    classes = [
        member
        for member in members
        if inspect.isclass(member[1]) and member[0] != strategy_meta.get("base")
    ]
    return {key: value for key, value in classes}
