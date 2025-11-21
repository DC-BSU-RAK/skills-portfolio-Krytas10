import tkinter as tk
from tkinter import messagebox
import random
import os

# Path to the jokes file (assumes it's in the same directory as this script)
JOKES_FILE = "randomJokes.txt"

def load_jokes():
    """Load and parse jokes from the file. Each joke: setup?punchline"""
    if not os.path.exists(JOKES_FILE):
        messagebox.showerror("Error", f"Could not find {JOKES_FILE}!")
        return []
    
    jokes = []
    try:
        with open(JOKES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # Most jokes use '?' to separate setup and punchline
                if "?" in line:
                    setup, punchline = line.split("?", 1)
                    # Clean up any extra spaces
                    setup = setup.strip() + "?"
                    punchline = punchline.strip()
                    jokes.append((setup, punchline))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read jokes file:\n{e}")
        return []
    
    return jokes

class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Alexa Tell Me a Joke")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f4f8")

        # Load jokes
        self.jokes = load_jokes()
        if not self.jokes:
            messagebox.showerror("No Jokes", "No jokes loaded. Exiting...")
            self.root.quit()

        self.current_joke = None

        # Title Label
        title_label = tk.Label(
            root,
            text="🤖 Alexa, Tell Me a Joke!",
            font=("Helvetica", 20, "bold"),
            bg="#f0f4f8",
            fg="#333"
        )
        title_label.pack(pady=20)

        # Joke display area (setup)
        self.setup_label = tk.Label(
            root,
            text="Click the button below to hear a joke!",
            font=("Arial", 16),
            wraplength=550,
            justify="center",
            bg="#f0f4f8",
            fg="#222"
        )
        self.setup_label.pack(pady=30)

        # Punchline label (initially hidden)
        self.punchline_label = tk.Label(
            root,
            text="",
            font=("Arial", 18, "italic"),
            wraplength=550,
            justify="center",
            bg="#f0f4f8",
            fg="#d35400"
        )
        self.punchline_label.pack(pady=20)

        # Frame for buttons
        button_frame = tk.Frame(root, bg="#f0f4f8")
        button_frame.pack(pady=20)

        # Button: Alexa tell me a joke
        self.tell_joke_btn = tk.Button(
            button_frame,
            text="Alexa tell me a Joke",
            font=("Helvetica", 14, "bold"),
            bg="#3498db",
            fg="white",
            width=20,
            height=2,
            command=self.tell_joke
        )
        self.tell_joke_btn.grid(row=0, column=0, padx=10)

        # Button: Show Punchline
        self.show_punchline_btn = tk.Button(
            button_frame,
            text="Show Punchline",
            font=("Helvetica", 14, "bold"),
            bg="#e67e22",
            fg="white",
            width=20,
            height=2,
            command=self.show_punchline,
            state=tk.DISABLED
        )
        self.show_punchline_btn.grid(row=0, column=1, padx=10)

        # Button: Next Joke
        self.next_joke_btn = tk.Button(
            button_frame,
            text="Next Joke",
            font=("Helvetica", 14),
            bg="#2ecc71",
            fg="white",
            width=15,
            command=self.tell_joke
        )
        self.next_joke_btn.grid(row=1, column=0, pady=10)

        # Button: Quit
        quit_btn = tk.Button(
            button_frame,
            text="Quit",
            font=("Helvetica", 14),
            bg="#e74c3c",
            fg="white",
            width=15,
            command=root.quit
        )
        quit_btn.grid(row=1, column=1, pady=10)

    def tell_joke(self):
        """Select and display a new random joke setup"""
        if not self.jokes:
            return

        self.current_joke = random.choice(self.jokes)
        setup, _ = self.current_joke

        self.setup_label.config(text=setup)
        self.punchline_label.config(text="")
        self.show_punchline_btn.config(state=tk.NORMAL)
        self.tell_joke_btn.config(state=tk.DISABLED)

    def show_punchline(self):
        """Reveal the punchline"""
        if self.current_joke:
            _, punchline = self.current_joke
            self.punchline_label.config(text=punchline)
            self.show_punchline_btn.config(state=tk.DISABLED)
            self.tell_joke_btn.config(state=tk.NORMAL)


# ——————————————— Run the app ———————————————
if __name__ == "__main__":
    root = tk.Tk()
    app = JokeApp(root)
    root.mainloop()