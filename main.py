from ui import QuizUserInterface
from quiz_engine import QuizEngine


def play_game():
    quiz = QuizEngine()     # sets up the game mechanics
    QuizUserInterface(quiz) # sets up the GUI


if __name__ == "__main__":
    play_game()
