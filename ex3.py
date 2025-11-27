import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

# ====================== Student Class ======================
class Student:
    def __init__(self, code, name, cw1, cw2, cw3, exam):
        self.code = int(code)
        self.name = name.strip()
        self.cw = [int(cw1), int(cw2), int(cw3)]
        self.exam = int(exam)

    def total_cw(self): return sum(self.cw)
    def total_score(self): return self.total_cw() + self.exam
    def percentage(self): return (self.total_score() / 160) * 100

    def grade(self):
        p = self.percentage()
        if p >= 70: return 'A', '#16a34a'
        elif p >= 60: return 'B', '#2563eb'
        elif p >= 50: return 'C', '#7c3aed'
        elif p >= 40: return 'D', '#d97706'
        else: return 'F', '#dc2626'

# ====================== File Handling ======================
FILENAME = "studentMarks.txt"

def load_students():
    if not os.path.exists(FILENAME):
        messagebox.showerror("Missing File", f"{FILENAME} not found!")
        return []
    try:
        with open(FILENAME, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        students = []
        for line in lines[1:]:
            parts = line.split(',')
            if len(parts) == 6:
                code, name, c1, c2, c3, exam = parts
                students.append(Student(code, name, c1, c2, c3, exam))
        return students
    except Exception as e:
        messagebox.showerror("Load Error", f"Could not read file:\n{e}")
        return []

def save_students(students):
    try:
        with open(FILENAME, 'w') as f:
            f.write(f"{len(students)}\n")
            for s in students:
                f.write(f"{s.code},{s.name},{s.cw[0]},{s.cw[1]},{s.cw[2]},{s.exam}\n")
    except Exception as e:
        messagebox.showerror("Save Error", f"Failed to save:\n{e}")

# ====================== Main App - Clean & Professional ======================
class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("1180x720")
        self.root.minsize(1000, 600)
        self.root.configure(bg="#f4f8fb")

        self.students = load_students()

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()

        self.create_widgets()
        self.show_summary()

    def configure_styles(self):
        # Clean, modern colors
        self.colors = {
            'bg': '#f4f8fb',
            'panel': '#ffffff',
            'accent': "#000000",      # Teal
            'accent_light': '#14b8a6',
            'text': '#1e293b',
            'light_text': '#64748b',
            'border': '#e2e8f0'
        }

        self.style.configure('.', background=self.colors['bg'], foreground=self.colors['text'])
        self.style.configure('Header.TLabel', font=('Helvetica', 26, 'bold'), foreground=self.colors['accent'])
        self.style.configure('Sub.TLabel', font=('Helvetica', 11), foreground=self.colors['light_text'])
        self.style.configure('Card.TFrame', background=self.colors['panel'], relief='flat', borderwidth=1)

        # Buttons
        self.style.configure('Action.TButton',
                             font=('Helvetica', 11),
                             padding=(20, 12),
                             background=self.colors['accent'],
                             foreground='white')
        self.style.map('Action.TButton',
                       background=[('active', self.colors['accent_light'])])

        # Treeview
        self.style.configure('Clean.Treeview', background='white', fieldbackground='white', rowheight=40,
                             font=('Segoe UI', 10), borderwidth=0)
        self.style.configure('Clean.Treeview.Heading', font=('Helvetica', 11, 'bold'),
                             background=self.colors['accent'], foreground='white')
        self.style.map('Clean.Treeview', background=[('selected', '#ccfbf1')])

    def create_widgets(self):
        # === Header ===
        header = tk.Frame(self.root, bg=self.colors['bg'])
        header.pack(fill='x', pady=(20, 10), padx=30)

        ttk.Label(header, text="Student Manager", style='Header.TLabel').pack()
        ttk.Label(header, text="Manage and analyze student performance records", style='Sub.TLabel').pack(pady=(2, 0))

        # === Main Layout ===
        container = tk.Frame(self.root, bg=self.colors['bg'])
        container.pack(fill='both', expand=True, padx=30, pady=10)

        # Left: Action Panel
        left = ttk.Frame(container, style='Card.TFrame', padding=20)
        left.pack(side='left', fill='y', padx=(0, 20))
        left.configure(width=300)
        left.pack_propagate(False)

        tk.Label(left, text="Menu", font=('Helvetica', 16, 'bold'), bg='white', fg=self.colors['text']).pack(anchor='w', pady=(0, 20))

        actions = [
            ("All Students", self.view_all),
            ("Search Student", self.view_individual),
            ("Top Performer", self.show_highest),
            ("Lowest Score", self.show_lowest),
            ("Sort Records", self.sort_records),
            ("Add Student", self.add_student),
            ("Delete Student", self.delete_student),
            ("Update Record", self.update_student),
        ]

        for text, cmd in actions:
            btn = ttk.Button(left, text=text, style='Action.TButton', command=cmd)
            btn.pack(fill='x', pady=6)

        # Right: Data Display
        right = ttk.Frame(container, style='Card.TFrame', padding=20)
        right.pack(side='right', fill='both', expand=True)

        # Summary Cards (Top)
        self.summary_frame = tk.Frame(right, bg='white')
        self.summary_frame.pack(fill='x', pady=(0, 20))

        # Treeview
        columns = ("Name", "ID", "CW Total", "Exam", "Total", "Percentage", "Grade")
        self.tree = ttk.Treeview(right, columns=columns, show='headings', style='Clean.Treeview')

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center', width=120)
        self.tree.column("Name", width=220, anchor='w')
        self.tree.column("Grade", width=80)

        scrollbar = ttk.Scrollbar(right, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Status bar
        self.status = tk.Label(self.root, text="Ready", anchor='w', bg='#e0f2fe', fg=self.colors['text'],
                               font=('Segoe UI', 10), padx=20, relief='flat')
        self.status.pack(side='bottom', fill='x')

    def update_summary(self):
        for widget in self.summary_frame.winfo_children():
            widget.destroy()

        if not self.students:
            return

        total = len(self.students)
        avg = sum(s.percentage() for s in self.students) / total
        top = max(self.students, key=lambda s: s.percentage())

        stats = [
            ("Total Students", str(total), "#64748b"),
            ("Class Average", f"{avg:.1f}%", "#0d9488"),
            ("Top Student", top.name.split()[0], "#16a34a"),
        ]

        for i, (label, value, color) in enumerate(stats):
            card = tk.Frame(self.summary_frame, bg='#f8fafc', relief='solid', bd=1)
            card.grid(row=0, column=i, padx=10, pady=8, sticky='ew')
            self.summary_frame.grid_columnconfigure(i, weight=1)

            tk.Label(card, text=label, font=('Helvetica', 10), fg='#94a3b8', bg='#f8fafc').pack(pady=(10, 2))
            tk.Label(card, text=value, font=('Helvetica', 18, 'bold'), fg=color, bg='#f8fafc').pack(pady=(0, 10))

    def show_summary(self):
        self.tree.delete(*self.tree.get_children())
        self.update_summary()
        self.status.config(text=f"Loaded {len(self.students)} student records • Ready")

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def display_students(self, student_list):
        self.clear_tree()
        self.update_summary()

        if not student_list:
            self.status.config(text="No records to display")
            return

        avg = sum(s.percentage() for s in student_list) / len(student_list)

        for s in student_list:
            grade_char, color = s.grade()
            perc = s.percentage()
            tag = f"grade_{grade_char}"
            self.tree.tag_configure(tag, foreground=color, font=('Segoe UI', 10, 'bold'))

            self.tree.insert("", "end", values=(
                s.name,
                s.code,
                s.total_cw(),
                s.exam,
                s.total_score(),
                f"{perc:.1f}%",
                grade_char
            ), tags=(tag,))

        self.status.config(text=f"Showing {len(student_list)} students • Average: {avg:.1f}%")

    def view_all(self):
        self.display_students(self.students)

    def view_individual(self):
        query = simpledialog.askstring("Search", "Enter Student ID or Name:")
        if not query: return
        query = query.strip()

        found = None
        for s in self.students:
            if str(s.code) == query or query.lower() in s.name.lower():
                found = s
                break

        if found:
            self.display_students([found])
            self.status.config(text=f"Found: {found.name} • Grade {found.grade()[0]}")
        else:
            messagebox.showwarning("Not Found", "No student matches your search.")

    def show_highest(self):
        if not self.students:
            messagebox.showinfo("Empty", "No records available.")
            return
        best = max(self.students, key=lambda s: s.percentage())
        self.display_students([best])
        self.status.config(text=f"Top performer: {best.name} — {best.percentage():.1f}%")

    def show_lowest(self):
        if not self.students:
            messagebox.showinfo("Empty", "No records available.")
            return
        worst = min(self.students, key=lambda s: s.percentage())
        self.display_students([worst])
        self.status.config(text=f"Lowest score: {worst.name} — {worst.percentage():.1f}%")

    def sort_records(self):
        if not self.students: return
        choice = simpledialog.askstring("Sort", "Sort by:\n1. Name\n2. ID\n3. Percentage\n\nEnter 1, 2, or 3:")
        if choice not in ["1", "2", "3"]:
            messagebox.showerror("Invalid", "Please enter 1, 2, or 3")
            return
        reverse = messagebox.askyesno("Order", "Descending? (Highest/Last first)")

        key_map = {"1": lambda s: s.name.lower(), "2": lambda s: s.code, "3": lambda s: s.percentage()}
        sorted_list = sorted(self.students, key=key_map[choice], reverse=reverse)
        self.display_students(sorted_list)

    def add_student(self):
        code = simpledialog.askinteger("Add", "Student ID (1000–9999):", minvalue=1000, maxvalue=9999)
        if not code or any(s.code == code for s in self.students):
            messagebox.showerror("Error", "Invalid or duplicate ID")
            return
        name = simpledialog.askstring("Add", "Full Name:")
        if not name or not name.strip(): return

        def ask(prompt, mx):
            while True:
                v = simpledialog.askinteger("Mark", prompt, minvalue=0, maxvalue=mx)
                if v is not None: return v
                if messagebox.askyesno("Cancel", "Cancel adding student?"): return None

        cw1 = ask("Coursework 1 (0–20):", 20)
        if cw1 is None: return
        cw2 = ask("Coursework 2 (0–20):", 20)
        if cw2 is None: return
        cw3 = ask("Coursework 3 (0–20):", 20)
        if cw3 is None: return
        exam = ask("Exam Mark (0–100):", 100)
        if exam is None: return

        self.students.append(Student(code, name, cw1, cw2, cw3, exam))
        save_students(self.students)
        messagebox.showinfo("Success", f"Student '{name}' added successfully")
        self.show_summary()

    def delete_student(self):
        s = self.find_student()
        if not s: return
        if messagebox.askyesno("Delete", f"Delete {s.name} ({s.code}) permanently?"):
            self.students.remove(s)
            save_students(self.students)
            messagebox.showinfo("Deleted", "Record removed")
            self.show_summary()

    def update_student(self):
        s = self.find_student()
        if not s: return

        fields = ["Name", "Coursework 1", "Coursework 2", "Coursework 3", "Exam Mark"]
        choice = simpledialog.askstring("Update", "Field to update:\n" + "\n".join(f"{i+1}. {f}" for i, f in enumerate(fields)))
        if not choice or not choice.isdigit() or int(choice) not in range(1, 6):
            return
        idx = int(choice) - 1

        if idx == 0:
            new = simpledialog.askstring("Update Name", "New name:", initialvalue=s.name)
            if new: s.name = new.strip()
        elif idx <= 3:
            new = simpledialog.askinteger("Update", f"New Coursework {idx} (0–20):", minvalue=0, maxvalue=20)
            if new is not None: s.cw[idx-1] = new
        else:
            new = simpledialog.askinteger("Update", "New Exam Mark (0–100):", minvalue=0, maxvalue=100)
            if new is not None: s.exam = new

        save_students(self.students)
        messagebox.showinfo("Updated", "Record updated successfully")
        self.show_summary()

    def find_student(self):
        query = simpledialog.askstring("Search", "Enter Student ID or Name:")
        if not query: return None
        query = query.strip()

        for s in self.students:
            if str(s.code) == query or query.lower() in s.name.lower():
                return s
        messagebox.showwarning("Not Found", "Student not found")
        return None

# ====================== Launch ======================
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()