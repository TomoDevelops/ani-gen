from random import choice, randint
import json


def choose_anime(genre, ranking):
    with open(f"./data/{genre}.json", 'r', encoding="utf-8") as file:
        data = json.load(file)
        if ranking > 0:
            return data[(randint(0, ranking))]
        else:
            return choice(data)
