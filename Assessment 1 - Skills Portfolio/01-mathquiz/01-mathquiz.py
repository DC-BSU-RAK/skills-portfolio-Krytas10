import tkinter as tk
from tkinter import messagebox
import random
import os
from PIL import Image, ImageTk

class MathQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maths Quiz - Final 950x550")
        
        # --- 1. FINAL DIMENSIONS ---
        self.win_width = 950
        self.win_height = 550
        self.center_x = self.win_width // 2
        self.center_y = self.win_height // 2
        
        self.root.geometry(f"{self.win_width}x{self.win_height}")
        self.root.resizable(False, False)
        
        # Game State
        self.score = 0
        self.question_count = 0
        self.difficulty = 0
        self.current_attempt = 1
        self.correct_answer = 0
        self.total_questions = 10
        self.time_left = 15
        self.timer_id = None

        # --- CANVAS SETUP ---
        self.canvas = tk.Canvas(root, width=self.win_width, height=self.win_height, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # --- BACKGROUND ---
        self.set_background("bg.jpg")

        # Fonts
        self.header_font = ("Arial", 36, "bold")
        self.rules_font = ("Arial", 18, "bold") 
        self.btn_font = ("Arial", 14, "bold")
        self.problem_font = ("Arial", 55, "bold")
        self.hud_font = ("Arial", 18, "bold")
        self.timer_font = ("Arial", 22, "bold")

        # Start
        self.displayWelcome()

    def set_background(self, filename):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, filename)
            original_image = Image.open(image_path)
            resized_image = original_image.resize((self.win_width, self.win_height), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized_image)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except Exception as e:
            print(f"Background Error: {e}")
            self.canvas.config(bg="#f0f0f0") 

    def clear_ui(self):
        """Clears UI elements."""
        self.canvas.delete("ui_element")
        self.canvas.delete("btn_shape")
        self.canvas.delete("btn_text")
        self.stop_timer()

    # ================== CUSTOM OVAL BUTTON (DARK BLUE) ==================
    def create_oval_button(self, x, y, text, command, width=200, height=50, bg_color="#00008B"):
        # Dark Blue Colors
        btn_color = bg_color  # DarkBlue default
        hover_color = "#0000CD" # MediumBlue (Lighter for hover)
        text_color = "white"

        btn_tag_shape = f"btn_shape_{text}_{random.randint(1,10000)}"
        btn_tag_text = f"btn_text_{text}_{random.randint(1,10000)}"

        x1 = x - width // 2
        x2 = x + width // 2
        
        # Draw Shape & Text
        self.canvas.create_line(x1, y, x2, y, fill=btn_color, width=height, capstyle=tk.ROUND, tags=("ui_element", btn_tag_shape))
        self.canvas.create_text(x, y, text=text, fill=text_color, font=self.btn_font, tags=("ui_element", btn_tag_text))

        # Animation Bindings
        def on_enter(e):
            self.canvas.itemconfig(btn_tag_shape, fill=hover_color)
            self.canvas.config(cursor="hand2")
        def on_leave(e):
            self.canvas.itemconfig(btn_tag_shape, fill=btn_color)
            self.canvas.config(cursor="")
        def on_click(e):
            command()

        for tag in [btn_tag_shape, btn_tag_text]:
            self.canvas.tag_bind(tag, "<Enter>", on_enter)
            self.canvas.tag_bind(tag, "<Leave>", on_leave)
            self.canvas.tag_bind(tag, "<Button-1>", on_click)

    # ================== PAGE 1: WELCOME PAGE ==================
    def displayWelcome(self):
        self.clear_ui()
        
        self.canvas.create_text(self.center_x, 180, text="MATH QUIZ", font=("Arial", 60, "bold"), fill="black", tags="ui_element")
        self.canvas.create_text(self.center_x, 260, text="CHALLENGE", font=("Arial", 60, "bold"), fill="darkblue", tags="ui_element")
        
        # Centered Start Button
        self.create_oval_button(self.center_x, 420, "LET'S START", self.displayRules, width=250, height=60)

    # ================== PAGE 2: RULES PAGE (NO FRAME) ==================
    def displayRules(self):
        self.clear_ui()
        
        # Title
        self.canvas.create_text(self.center_x, 130, text="GAME RULES", font=self.header_font, fill="darkred", tags="ui_element")

        rules_text = (
            "1. You have 10 Questions to solve.\n\n"
            "2. Correct Answer (1st Try): +10 Points\n\n"
            "3. Correct Answer (2nd Try): +5 Points\n\n"
            "4. Time Limit: 15 Seconds per question."
        )
        
        # --- NO RECTANGLE HERE (DIRECT ON BG) ---
        # Padding adjustment: Y=300 looks good for center
        
        # Text shadow effect create karne ke liye pehle White text thora offset par banayenge
        # taake agar background dark ho ya light, text pop kare.
        self.canvas.create_text(self.center_x + 2, 300 + 2, text=rules_text, font=self.rules_font, fill="white", justify="center", tags="ui_element") # Shadow
        self.canvas.create_text(self.center_x, 300, text=rules_text, font=self.rules_font, fill="black", justify="center", tags="ui_element") # Main Text
        
        # Next Button
        self.create_oval_button(self.center_x, 480, "NEXT >", self.displayDifficulty, width=220, height=55)

    # ================== PAGE 3: DIFFICULTY PAGE ==================
    def displayDifficulty(self):
        self.clear_ui()
        
        self.canvas.create_text(self.center_x, 130, text="Select Difficulty Level", font=self.header_font, fill="black", tags="ui_element")
        
        # Buttons vertically stacked in center
        self.create_oval_button(self.center_x, 220, "1. Easy (1 Digit)", lambda: self.start_quiz(1), width=280, height=45)
        self.create_oval_button(self.center_x, 300, "2. Moderate (2 Digits)", lambda: self.start_quiz(2), width=280, height=45)
        self.create_oval_button(self.center_x, 380, "3. Advanced (4 Digits)", lambda: self.start_quiz(3), width=280, height=45)
        
        # Back Button
        self.create_oval_button(self.center_x, 480, "< BACK", self.displayRules, width=180, height=50)

    # ================== GAME LOGIC ==================
    def start_quiz(self, level):
        self.difficulty = level
        self.score = 0
        self.question_count = 0
        self.next_question_setup()

    def next_question_setup(self):
        if self.question_count < self.total_questions:
            self.question_count += 1
            self.current_attempt = 1
            self.displayProblem()
        else:
            self.displayResults()

    def randomInt(self):
        if self.difficulty == 1: return random.randint(0, 9)
        elif self.difficulty == 2: return random.randint(10, 99)
        elif self.difficulty == 3: return random.randint(1000, 9999)
        return 0

    def decideOperation(self):
        return random.choice(['+', '-'])

    # --- TIMER ---
    def start_timer(self):
        self.stop_timer()
        self.time_left = 15
        self.update_timer()

    def stop_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def update_timer(self):
        try:
            self.canvas.itemconfig(self.timer_text_id, text=f"Time: {self.time_left}s")
            # Warning Color Red
            if self.time_left <= 5:
                self.canvas.itemconfig(self.timer_text_id, fill="red")
            else:
                self.canvas.itemconfig(self.timer_text_id, fill="blue")
        except: pass

        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.handle_timeout()

    def handle_timeout(self):
        self.stop_timer()
        if self.current_attempt == 1:
            self.current_attempt = 2
            self.canvas.itemconfig(self.feedback_text_id, text="Time's Up! Last Chance!", fill="red")
            self.start_timer()
        else:
            messagebox.showinfo("Time Out", f"Time is up! The correct answer was {self.correct_answer}")
            self.next_question_setup()

    # ================== PAGE 4: QUIZ PAGE (FIXED PADDING) ==================
    def displayProblem(self):
        self.clear_ui()
        
        num1 = self.randomInt()
        num2 = self.randomInt()
        operation = self.decideOperation()
        
        if operation == '+': self.correct_answer = num1 + num2
        else: self.correct_answer = num1 - num2
            
        # --- HUD (Padding Increase) ---
        # Moved X,Y from 30,30 to 50,60 for better spacing
        self.canvas.create_text(50, 60, text=f"Q: {self.question_count}/{self.total_questions}", 
                                font=self.hud_font, fill="black", anchor="nw", tags="ui_element")
        
        self.canvas.create_text(self.win_width - 50, 60, text=f"Score: {self.score}", 
                                font=self.hud_font, fill="darkgreen", anchor="ne", tags="ui_element")
        
        # --- TIMER (Lowered Position) ---
        # Moved Y from 60 to 120 (Clear of top clip art)
        self.timer_text_id = self.canvas.create_text(self.center_x, 120, text="Time: 15s", 
                                                     font=self.timer_font, fill="blue", tags="ui_element")
        
        # --- PROBLEM (Centered) ---
        problem_text = f"{num1} {operation} {num2} ="
        self.canvas.create_text(self.center_x, 240, text=problem_text, font=self.problem_font, fill="black", tags="ui_element")
        
        # --- INPUT FIELD ---
        self.answer_entry = tk.Entry(self.root, font=("Arial", 28, "bold"), justify='center', bd=4, width=8)
        self.canvas.create_window(self.center_x, 340, window=self.answer_entry, tags="ui_element")
        self.answer_entry.focus()
        self.answer_entry.bind('<Return>', lambda event: self.check_answer_trigger())
        
        # --- SUBMIT BUTTON ---
        self.create_oval_button(self.center_x, 430, "SUBMIT", self.check_answer_trigger, width=200, height=55)
        
        # --- FEEDBACK TEXT (Bottom) ---
        self.feedback_text_id = self.canvas.create_text(self.center_x, 500, text="", font=("Arial", 18, "bold"), fill="black", tags="ui_element")

        self.start_timer()

    def check_answer_trigger(self):
        try:
            val = self.answer_entry.get()
            if not val: return 
            user_val = int(val)
            self.isCorrect(user_val)
        except ValueError:
            self.canvas.itemconfig(self.feedback_text_id, text="Please enter numbers only!", fill="red")
            self.answer_entry.delete(0, tk.END)

    def isCorrect(self, user_answer):
        if user_answer == self.correct_answer:
            self.stop_timer()
            
            # --- POINTS LOGIC & FEEDBACK ---
            if self.current_attempt == 1:
                points = 10
                msg = "Correct! +10 Points!"
            else:
                points = 5
                msg = "Correct! +5 Points!"
            
            self.score += points
            
            self.canvas.itemconfig(self.feedback_text_id, text=msg, fill="green")
            self.root.update()
            self.root.after(1000, self.next_question_setup)
        else:
            if self.current_attempt == 1:
                self.current_attempt = 2
                self.canvas.itemconfig(self.feedback_text_id, text="Wrong! Try Again (+5 pts possible)", fill="red")
                self.answer_entry.delete(0, tk.END)
                self.start_timer()
            else:
                self.stop_timer()
                messagebox.showinfo("Result", f"Wrong again. Answer: {self.correct_answer}")
                self.next_question_setup()

    # ================== PAGE 5: RESULT PAGE ==================
    def displayResults(self):
        self.clear_ui()
        
        grade = "F"
        if self.score > 90: grade = "A+"
        elif self.score > 80: grade = "A"
        elif self.score > 70: grade = "B"
        elif self.score > 60: grade = "C"
        
        self.canvas.create_text(self.center_x, 150, text="QUIZ COMPLETED", font=("Arial", 36, "bold"), fill="black", tags="ui_element")
        self.canvas.create_text(self.center_x, 240, text=f"Final Score: {self.score} / 100", font=("Arial", 28, "bold"), fill="darkblue", tags="ui_element")
        self.canvas.create_text(self.center_x, 320, text=f"Rank: {grade}", font=("Arial", 48, "bold"), fill="purple", tags="ui_element")
        
        # --- NEW BUTTONS (PLAY AGAIN & EXIT) ---
        self.create_oval_button(self.center_x - 150, 450, "PLAY AGAIN", self.displayWelcome, width=220, height=60, bg_color="green")
        self.create_oval_button(self.center_x + 150, 450, "EXIT", self.root.destroy, width=220, height=60, bg_color="red")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = MathQuizApp(root)
        root.mainloop()
    except ImportError:
        root = tk.Tk()
        tk.Label(root, text="Error: Please run 'pip install pillow'", fg="red").pack()
        root.mainloop()