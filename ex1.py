

import tkinter as tk
from tkinter import messagebox
import random

class MathQuizGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Arithmetic Quiz")
        self.root.geometry("350x225")   

        # Game variables
        self.difficulty = None
        self.question_count = 0
        self.score = 0
        self.first_attempt = True
        self.correct_answer = None

        self.displayMenu()

    # Display
    def displayMenu(self):
        self.clearWindow()

        tk.Label(self.root, text="DIFFICULTY LEVEL", font=("Arial", 15)).pack(pady=15)

        tk.Button(self.root, text="1. Easy (1-digit numbers)", width=30, bg="#5EC462", fg="black",
                  command=lambda: self.startQuiz(1)).pack(pady=8)
        tk.Button(self.root, text="2. Moderate (2-digit numbers)", width=30, bg="#B38D54", fg="black",
                  command=lambda: self.startQuiz(2)).pack(pady=8)
        tk.Button(self.root, text="3. Advanced (4-digit numbers)", width=30, bg="#B85D57", fg="black",
                  command=lambda: self.startQuiz(3)).pack(pady=8)

    # Start Quiz
    def startQuiz(self, level):
        self.difficulty = level
        self.question_count = 0
        self.score = 0

        self.nextQuestion()

    # Random Int
    def randomInt(self):
        if self.difficulty == 1:
            return random.randint(1, 9)
        elif self.difficulty == 2:
            return random.randint(10, 99)
        else:
            return random.randint(1000, 9999)

    # Decide Operation
    def decideOperation(self):
        return random.choice(['+', '-'])

    # Display Operation
    def nextQuestion(self):
        if self.question_count == 10:
            self.displayResults()
            return

        self.question_count += 1
        self.first_attempt = True

        # Generate problem
        self.num1 = self.randomInt()
        self.num2 = self.randomInt()
        self.op = self.decideOperation()

        if self.op == '+':
            self.correct_answer = self.num1 + self.num2
        else:
            self.correct_answer = self.num1 - self.num2

        self.displayProblem()

    def displayProblem(self):
        self.clearWindow()

        q_text = f"Question {self.question_count} of 10"
        tk.Label(self.root, text=q_text, font=("Arial", 14)).pack(pady=10)

        problem_text = f"{self.num1} {self.op} {self.num2} ="
        tk.Label(self.root, text=problem_text, font=("Arial", 20)).pack(pady=10)

        self.answer_entry = tk.Entry(self.root, font=("Arial", 14))
        self.answer_entry.pack()
        self.answer_entry.focus()
        self.answer_entry.bind("<Return>", lambda event: self.checkAnswer())
        tk.Button(self.root, text="Submit Answer", bg="#4D8FD1", fg="black", command=self.checkAnswer).pack(pady=15)

    # Is correct
    def checkAnswer(self):
        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a number.")
            return

        if user_answer == self.correct_answer:
            if self.first_attempt:
                self.score += 10
                messagebox.showinfo("Correct!", "Correct! +10 points")
            else:
                self.score += 5
                messagebox.showinfo("Correct!", "Correct! +5 points")
            self.nextQuestion()
        else:
            if self.first_attempt:
                self.first_attempt = False
                messagebox.showwarning("Incorrect", "Wrong answer! Try again.")
            else:
                messagebox.showinfo("Incorrect", f"Wrong again! Correct answer was {self.correct_answer}")
                self.nextQuestion()

    # Display results
    def displayResults(self):
        self.clearWindow()

        grade = self.calculateGrade(self.score)

        tk.Label(self.root, text=f"Your Score: {self.score}/100", font=("Arial", 20)).pack(pady=10)
        tk.Label(self.root, text=f"Grade: {grade}", font=("Arial", 18)).pack(pady=10)

        tk.Button(self.root, text="Play Again", bg="#5EC462", fg="black" , command=self.displayMenu).pack(pady=10)
        tk.Button(self.root, text="Exit", bg="#B85D57", fg="black" , command=self.root.quit).pack(pady=10)

    def calculateGrade(self, score):
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
        else:
            return "F"

    # Clear Window
    def clearWindow(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# RUN APP
root = tk.Tk()
app = MathQuizGUI(root)
root.mainloop()
