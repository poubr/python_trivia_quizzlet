from tkinter import *
from quiz_engine import QuizEngine


# HANDLING GUI:
class QuizUserInterface:

    def __init__(self, quiz_engine: QuizEngine):
        # import quiz engine
        self.quiz_engine = quiz_engine

        self.root = Tk()
        self.root.title("Trivia Quizzlet")
        self.root.config(padx=10, pady=10, background="black")

        self.font = ("Courier", 25, "bold")

        self.question_bg_img = PhotoImage(file="images/question_bg.png")
        self.correct_bg_img = PhotoImage(file="images/correct_bg.png")
        self.wrong_bg_img = PhotoImage(file="images/wrong_bg.png")
        true_answer_img = PhotoImage(file="images/true_answer.png")
        false_answer_img = PhotoImage(file="images/false_answer.png")

        self.answered_correctly = None

        # WIDGETS
        self.score = 0
        self.score_label = Label(text=f"Score: {self.score}",
                                 fg="white",
                                 bg="black",
                                 highlightthickness=0,
                                 font=self.font)
        self.score_label.grid(row=0, column=0)

        self.progress_label = Label(text=f"{self.quiz_engine.question_number} / 10",
                                    fg="white",
                                    bg="black",
                                    highlightthickness=0,
                                    font=self.font)
        self.progress_label.grid(row=0, column=1)

        self.canvas = Canvas(width=450,
                             height=300,
                             bd=0,
                             highlightthickness=0)
        self.canvas.config(bg="black")
        self.canvas.grid(row=1, column=0, columnspan=2)

        self.question_bg = self.canvas.create_image(225, 150, image=self.question_bg_img)
        self.question_text = self.canvas.create_text(225,
                                                     150,
                                                     text="Question goes here.",
                                                     font=self.font,
                                                     fill="white",
                                                     width=350)

        self.true_answer_button = Button(image=true_answer_img, command=self.check_true, highlightthickness=0)
        self.true_answer_button.grid(row=2, column=0, pady=20)

        self.false_answer_button = Button(image=false_answer_img, command=self.check_false, highlightthickness=0)
        self.false_answer_button.grid(row=2, column=1, pady=20)

        self.get_next_question()
        self.root.mainloop()

    # Fetches the next questions and updates GUI
    def get_next_question(self):
        self.canvas.itemconfig(self.question_bg, image=self.question_bg_img)
        self.progress_label.config(text=f"{self.quiz_engine.question_number} / 10")
        next_question = self.quiz_engine.next_question()

        # if there are no more questions available, checks for reset:
        if next_question == "end":
            self.canvas.itemconfig(self.question_text,
                                   text=f"The end! Your score is {self.score} / 10.")
            self.true_answer_button.config(state="disabled")
            self.false_answer_button.config(state="disabled")

        # sets up next questions if available:
        else:
            self.true_answer_button.config(state="normal")
            self.false_answer_button.config(state="normal")
            self.canvas.itemconfig(self.question_text, text=next_question)

    # checks if the "is true" answer is correct
    def check_true(self):
        self.answered_correctly = self.quiz_engine.check_answer("True")
        self.process_answer()

    # checks if the "is false" answer is correct
    def check_false(self):
        self.answered_correctly = self.quiz_engine.check_answer("False")
        self.process_answer()

    # processes the user answer and updates GUI
    def process_answer(self):
        if self.answered_correctly:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.canvas.itemconfig(self.question_bg, image=self.correct_bg_img)
        else:
            self.canvas.itemconfig(self.question_bg, image=self.wrong_bg_img)

        self.quiz_engine.question_number += 1

        # disabled buttons so user cannot answer next question before it appears
        self.true_answer_button.config(state="disabled")
        self.false_answer_button.config(state="disabled")

        # delay so that user can see the answer
        self.root.after(1500, self.get_next_question)
