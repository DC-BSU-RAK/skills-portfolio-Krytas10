import tkinter as tk
from tkinter import messagebox
import random
import os
import pyttsx3  # Extended Learning: Library for voice output
from PIL import Image, ImageTk 

class JokeApp:
    """
    Main class for the Joke Application.
    Encapsulates GUI rendering, file handling, and game logic.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa - The Talking Joker")
        
        # --- Window Configuration ---
        self.win_width = 800
        self.win_height = 600
        # Calculating center coordinates for precise element placement
        self.center_x = self.win_width // 2
        self.center_y = self.win_height // 2
        
        self.root.geometry(f"{self.win_width}x{self.win_height}")
        self.root.resizable(False, False)
        
        # --- Extended Feature: Voice Engine ---
        # Initializes the text-to-speech engine for audio feedback
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)    # Adjusting speaking rate
        except:
            self.engine = None
            print("Warning: Voice Engine could not be initialized.")

        # --- Data Initialization ---
        self.jokes_list = []
        self.current_setup = ""
        self.current_punchline = ""
        
        # --- UI Setup ---
        # Utilizing Canvas widget to allow layering of text over background images
        self.canvas = tk.Canvas(root, width=self.win_width, height=self.win_height, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # --- Asset Management ---
        # Loading background and joke data with error handling
        if not self.set_background("bg-jokes.jpeg"):
            self.set_background("bg-jokes.jpg")
            
        self.load_jokes("randomJokes.txt")

        # --- Typography ---
        self.setup_font = ("Arial", 22, "bold") 
        self.punchline_font = ("Comic Sans MS", 26, "bold italic") # Stylized font for impact
        self.btn_font = ("Arial", 14, "bold")

        # Initialize the application state
        self.show_start_screen()

    def set_background(self, filename):
        """
        Loads and resizes the background image dynamically.
        Uses os.path to ensure cross-platform compatibility.
        """
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, filename)
            
            original_image = Image.open(image_path)
            # High-quality resampling for better visual fidelity
            resized_image = original_image.resize((self.win_width, self.win_height), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized_image)
            
            # Rendering image on the lowest layer of the canvas
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
            return True
        except Exception as e:
            print(f"Error loading background: {e}")
            self.canvas.config(bg="#FFD700") # Fallback color
            return False

    def load_jokes(self, filename):
        """
        Reads jokes from an external text file.
        Splits data into Setup and Punchline based on the '?' delimiter.
        """
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, filename)
            with open(file_path, "r", encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    if "?" in line:
                        parts = line.strip().split("?")
                        setup = parts[0] + "?"
                        punchline = parts[1]
                        self.jokes_list.append((setup, punchline))
            if not self.jokes_list: raise ValueError
        except Exception:
            # Graceful error handling with a default joke
            self.jokes_list = [("Knock knock?", "Who's there? File not found!")]

    def clear_ui(self):
        """Resets the screen by removing dynamic UI elements."""
        self.canvas.delete("ui_element")
        self.canvas.delete("btn_shape")
        self.canvas.delete("btn_text")

    # ================== EXTENDED FEATURES (Animation & Audio) ==================
    def speak(self, text):
        """Outputs audio using the initialized TTS engine."""
        if self.engine:
            self.engine.say(text)
            self.engine.runAndWait()

    def typewriter_effect(self, text, x, y, font, color, delay=50, speak_after=False):
        """
        Recursively renders text character-by-character to simulate typing.
        Adds visual interest and engagement.
        """
        text_id = self.canvas.create_text(x, y, text="", font=font, fill=color, width=600, justify="center", tags="ui_element")
        
        def update_text(current_text, index):
            if index < len(text):
                current_text += text[index]
                self.canvas.itemconfig(text_id, text=current_text)
                self.root.after(delay, update_text, current_text, index + 1)
            elif speak_after:
                self.root.after(100, lambda: self.speak(text))

        update_text("", 0)

    # ================== CUSTOM WIDGETS ==================
    def create_custom_button(self, x, y, text, command, width=220, height=50, bg_color="#00008B"):
        """
        Creates a custom vector-based button on the Canvas.
        Includes hover effects for better User Experience (UX).
        """
        hover_color = "#4169E1"
        text_color = "white"
        
        # Tags for event binding
        btn_tag_shape = f"btn_shape_{text}_{random.randint(1,10000)}"
        btn_tag_text = f"btn_text_{text}_{random.randint(1,10000)}"
        x1, x2 = x - width // 2, x + width // 2
        
        # Drawing pill shape
        self.canvas.create_line(x1, y, x2, y, fill=bg_color, width=height, capstyle=tk.ROUND, tags=("ui_element", btn_tag_shape))
        self.canvas.create_text(x, y, text=text, fill=text_color, font=self.btn_font, tags=("ui_element", btn_tag_text))

        # Event Listeners for interactivity
        def on_enter(e):
            self.canvas.itemconfig(btn_tag_shape, fill=hover_color)
            self.root.config(cursor="hand2")
        def on_leave(e):
            self.canvas.itemconfig(btn_tag_shape, fill=bg_color)
            self.root.config(cursor="")
        def on_click(e): command()

        for tag in [btn_tag_shape, btn_tag_text]:
            self.canvas.tag_bind(tag, "<Enter>", on_enter)
            self.canvas.tag_bind(tag, "<Leave>", on_leave)
            self.canvas.tag_bind(tag, "<Button-1>", on_click)

    # ================== APP STATES ==================
    def show_start_screen(self):
        """Renders the initial landing page."""
        self.clear_ui()
        self.canvas.create_text(self.center_x, 250, text="Alexa Joke Assistant", font=("Arial", 40, "bold"), fill="black", tags="ui_element")
        self.create_custom_button(self.center_x, 350, "Tell me a Joke", self.get_random_joke, width=250, height=60, bg_color="#379D27")

    def get_random_joke(self):
        """Randomly selects a joke tuple from the list."""
        if self.jokes_list:
            joke = random.choice(self.jokes_list)
            self.current_setup = joke[0]
            self.current_punchline = joke[1]
            self.show_setup_state()

    def show_setup_state(self):
        """Displays the setup phase of the joke."""
        self.clear_ui()
        self.typewriter_effect(self.current_setup, self.center_x, 220, self.setup_font, "black", speak_after=True)
        
        self.create_custom_button(self.center_x, 350, "Show Punchline", self.show_punchline_state, width=220, height=55, bg_color="#00008B")
        self.create_custom_button(self.win_width - 80, self.win_height - 40, "Quit", self.root.destroy, width=100, height=30, bg_color="#B22222")

    def show_punchline_state(self):
        """Displays the punchline phase with dynamic styling."""
        self.clear_ui()
        
        # Retain setup text
        self.canvas.create_text(self.center_x, 200, text=self.current_setup, font=self.setup_font, fill="#333", width=600, justify="center", tags="ui_element")
        
        # Dynamic color selection for visual appeal
        colors = ["#8B0000", "#4B0082", "#006400", "#800080", "#FF4500"]
        punch_color = random.choice(colors)
        
        # Animate punchline
        self.typewriter_effect(self.current_punchline, self.center_x, 300, self.punchline_font, punch_color, speak_after=True)
        
        self.create_custom_button(self.center_x, 440, "Next Joke", self.get_random_joke, width=220, height=55, bg_color="#006400")
        self.create_custom_button(self.win_width - 80, self.win_height - 40, "Quit", self.root.destroy, width=100, height=30, bg_color="#B22222")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = JokeApp(root)
        root.mainloop()
    except Exception as e:
        print(e)