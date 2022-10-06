import requests
from html import unescape


# handles question mechanics and answers
class QuizEngine:

    def __init__(self):
        self.questions = None
        self.question_number = 1

        self.generate_questions()

    # returns next question if there are questions available, "end" if not
    def next_question(self):
        if self.question_number <= len(self.questions):
            question = self.questions[self.question_number-1][0]
            return f"{self.question_number}. {unescape(question)}"
        else:
            return "end"

    # compares if user answer is the same as actual answer, returns bool
    def check_answer(self, user_answer: str):
        answer = self.questions[self.question_number-1][1]
        return answer == user_answer

    def generate_questions(self):
        parameters = {
            "amount": 10,
            "type": "boolean"
        }

        data = requests.get("https://opentdb.com/api.php", params=parameters)
        data.raise_for_status()
        self.questions = [(question["question"], question["correct_answer"]) for question in data.json()["results"]]

