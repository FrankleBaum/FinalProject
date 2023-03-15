import csv
import random
import tkinter as tk
from tkinter import messagebox
import sys

class QuizApp:
    def __init__(self, csv_file):
        self.questions = self.load_questions(csv_file)
        self.current_question = 0
        self.score = 0
        self.init_gui()

    def init_gui(self):
        self.window = tk.Tk()
        self.window.title("Quiz App")
        self.question_label = tk.Label(self.window, font=('Arial', 14), wraplength=400, justify='center')
        self.question_label.pack(pady=20)
        self.choice_buttons = []
        for i in range(4):
            button = tk.Button(self.window, font=('Arial', 12), width=30, height=2, command=lambda index=i: self.answer_question(index))
            self.choice_buttons.append(button)
            button.pack(pady=5)
        self.score_label = tk.Label(self.window, font=('Arial', 12))
        self.score_label.pack(pady=20)
        self.next_button = tk.Button(self.window, text="Next", font=('Arial', 12), width=10, height=2, command=self.show_next_question)
        self.next_button.pack(pady=10)
        self.show_question()
        self.window.mainloop()

    def load_questions(self, csv_file):
        questions = []
        with open(csv_file, newline='') as file:
            reader = csv.reader(file)
            next(reader)  # skip header row
            for row in reader:
                if len(row) != 5:
                    raise ValueError(f"Invalid number of fields in row: {row}")
                question, answer, decoy1, decoy2, decoy3 = row
                questions.append((question, answer, decoy1, decoy2, decoy3))
        random.shuffle(questions)
        return questions

    def show_question(self):
        question, answer, decoy1, decoy2, decoy3 = self.questions[self.current_question]
        choices = random.sample([decoy1, decoy2, decoy3, answer], k=4)
        self.question_label.config(text=question)
        self.score_label.config(text=f"Score: {self.score}")
        for i in range(4):
            self.choice_buttons[i].config(text=choices[i], bg="white", state='normal')

    def answer_question(self, index):
        question, answer, decoy1, decoy2, decoy3 = self.questions[self.current_question]
        selected_choice = self.choice_buttons[index].cget('text')
        if selected_choice == answer:
            self.score += 1
            self.choice_buttons[index].config(bg="green")
        else:
            self.choice_buttons[index].config(bg="red")
            for i in range(4):
                if self.choice_buttons[i].cget('text') == answer:
                    self.choice_buttons[i].config(bg="green")
        for button in self.choice_buttons:
            button.config(state='disabled')
        self.next_button.config(state='normal')

    def show_next_question(self):
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.show_question()
            for button in self.choice_buttons:
                button.config(state='normal', bg="white")
            self.next_button.config(state='disabled')
        else:
            messagebox.showinfo("Quiz Finished", f"Final score: {self.score} out of {len(self.questions)}")
            self.window.destroy()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python shuffle_questions_gui.py <filename>')
        sys.exit(1)
    filename = sys.argv[1]
    app = QuizApp(filename)