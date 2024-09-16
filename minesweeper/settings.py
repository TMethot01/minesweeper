# settings.py

class GameSettings:
    def __init__(self, difficulty='beginner'):
        self.difficulty = difficulty
        self.width, self.height, self.mines = self.get_settings()

    def get_settings(self):
        if self.difficulty == 'beginner':
            return 9, 9, 10
        elif self.difficulty == 'intermediate':
            return 16, 16, 40
        elif self.difficulty == 'expert':
            return 30, 16, 99
        else:
            raise ValueError("Invalid difficulty level")