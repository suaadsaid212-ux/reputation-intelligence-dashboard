import random

def get_social_score(entity):

    return {

        "mentions":
        random.randint(100, 10000),

        "sentiment":
        round(random.uniform(-1, 1), 2),

        "engagement":
        random.randint(1000, 100000)

    }
