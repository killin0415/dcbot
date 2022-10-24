import json
import random


class AdvencedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__jsonencode__'):
            return obj.__jsonencode__()
        return json.JSONEncoder.default(self, obj)


class Player():
    def __init__(self, id, name, level=0, exp=0,rank=-1, ranklimit=89, fb = [89,144]) -> None:
        self.id = id
        self.name = name
        self.level = level
        self.exp = exp
        self.ranklimit = ranklimit
        self.fb = fb
        self.rank = rank

    def __jsonencode__(self):
        return {
            "id": self.id,
            "name": self.name,
            "level": self.level,
            "exp": self.exp,
            "ranklimit": self.ranklimit,
            "rank": self.rank,
            "fb": self.fb
        }

    def update(self):
        exp = random.randint(0, 5)
        self.exp += exp
        if self.exp >= self.ranklimit:
            self.level += 1
            self.exp -= self.ranklimit
            self.ranklimit = self.fb[1]
            self.fb[0], self.fb[1] = self.fb[1], self.fb[0]+self.fb[1]
