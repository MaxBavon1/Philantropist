import json

__all__ = ["Data"]

""" Loads all the data/configurations needed to play the game """


class Data:

    __slots__ = ["path", "progress", "entities", "levels"]

    def __init__(self) -> None:
        self.path = "data/"
        self.progress = {}
        self.entities = {}
        self.levels = {}

    def load_progress(self):
        with open(self.path + "progress.json", "r") as progress_file:
            self.progress = json.load(progress_file)

    def save_progress(self):
        with open(self.path + "progress.json", "w") as progress_file:
            json.dump(self.progress, progress_file, indent=4)
        
    def load_game_data(self):
        with open(self.path + "entities.json", "r") as json_file:
            self.entities = json.load(json_file)

        with open(self.path + "levels.json", "r") as json_file:
            self.levels = json.load(json_file)