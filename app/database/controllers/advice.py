from database import database, Collections

from random import randint

class Advice:
    @classmethod
    def get_advice(cls):
        advices = list(database[Collections.ADVICES].find(
            {},
            {"_id": 0}
        ))

        return advices[randint(0, len(advices) - 1)]
