import tkinter as tk
from tkinter import ttk, messagebox
import os

# --- Configuration ---
FILENAME = "studentMarks.txt"
THEME_COLOR = "#0f172a"  # Navy Blue
ACCENT_COLOR = "#0ea5e9" # Teal Blue
BG_COLOR = "#f1f5f9"     # Light Background

class Student:
    def __init__(self, code, name, cw1, cw2, cw3, exam):
        self.code = int(code)
        self.name = name.strip()
        self.cw = [int(cw1), int(cw2), int(cw3)]
        self.exam = int(exam)

    def total_cw(self): return sum(self.cw)
    def total_score(self): return self.total_cw() + self.exam
    def percentage(self): return (self.total_score() / 160) * 100

    def get_grade_info(self):
        p = self.percentage()
        if p >= 70: return 'A'
        elif p >= 60: return 'B'
        elif p >= 50: return 'C'
        elif p >= 40: return 'D'
        else: return 'F'

class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Data Manager Pro")
        self.root.geometry("1100x700")
        self.root.configure(bg=BG_COLOR)
        
        self.students = []
        self.load_data()
        
        # UI Components
        self.setup_styles()
        self.create_header()
        self.create_dashboard_cards()
        self.create_main_area()
        self.refresh_table()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="white", foreground="black", rowheight=30, font=('Segoe UI', 10))
        style.configure("Treeview.Heading", font=('Segoe UI', 10, 'bold'), background=THEME_COLOR, foreground="white", relief="flat")
        style.map("Treeview", background=[('selected', ACCENT_COLOR)])

    # --- File Handling ---
    def get_file_path(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_dir, FILENAME)

    def load_data(self):
        file_path = self.get_file_path()
        if not os.path.exists(file_path): return
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
                for line in lines[1:]:
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) == 6:
                            self.students.append(Student(*parts))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load: {e}")

    def save_data(self):
        try:
            with open(self.get_file_path(), 'w') as f:
                f.write(f"{len(self.students)}\n")
                for s in self.students:
                    f.write(f"{s.code},{s.name},{s.cw[0]},{s.cw[1]},{s.cw[2]},{s.exam}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    # --- GUI Layout ---
    def create_header(self):
        header = tk.Frame(self.root, bg=THEME_COLOR, height=60)
        header.pack(fill='x')
        tk.Label(header, text="🎓 Student Record Manager", font=("Segoe UI", 20, "bold"), bg=THEME_COLOR, fg="white").pack(side='left', padx=20, pady=10)

    def create_dashboard_cards(self):
        stats_frame = tk.Frame(self.root, bg=BG_COLOR)
        stats_frame.pack(fill='x', padx=20, pady=15)
        self.card_total = self.create_card(stats_frame, "Total Students", "0", "#3b82f6")
        self.card_avg = self.create_card(stats_frame, "Class Average", "0%", "#10b981")
        self.card_top = self.create_card(stats_frame, "Highest Score", "-", "#f59e0b")

    def create_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg="white", highlightbackground=color, highlightthickness=2, padx=15, pady=10)
        card.pack(side='left', fill='x', expand=True, padx=5)
        tk.Label(card, text=title, font=("Segoe UI", 9), bg="white", fg="#64748b").pack(anchor='w')
        val_lbl = tk.Label(card, text=value, font=("Segoe UI", 18, "bold"), bg="white", fg="#1e293b")
        val_lbl.pack(anchor='w')
        return val_lbl

    def create_main_area(self):
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Menu
        sidebar = tk.Frame(main_frame, bg="white", width=220, relief="groove", bd=1)
        sidebar.pack(side='left', fill='y', padx=(0, 15))
        sidebar.pack_propagate(False)

        # Search
        tk.Label(sidebar, text="Search Record", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor='w', padx=10, pady=(15, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_search)
        tk.Entry(sidebar, textvariable=self.search_var, font=("Segoe UI", 10), bg="#f1f5f9", relief="flat").pack(fill='x', padx=10, pady=5)

        # Buttons
        tk.Label(sidebar, text="Menu Options", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor='w', padx=10, pady=(15, 5))
        btns = [
            ("View All Records", self.refresh_table, "#475569"),
            ("Show Highest Score", self.show_highest, "#0891b2"),
            ("Show Lowest Score", self.show_lowest, "#0891b2"),
            ("Add Student", self.add_student_form, ACCENT_COLOR), # Updated Function
            ("Update Selected", self.update_student_form, "#6366f1"), # Updated Function
            ("Delete Selected", self.delete_student, "#ef4444")
        ]
        for txt, cmd, col in btns:
            tk.Button(sidebar, text=txt, bg=col, fg="white", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=cmd).pack(fill='x', padx=10, pady=4, ipady=5)

        # Table
        table_frame = tk.Frame(main_frame, bg="white")
        table_frame.pack(side='right', fill='both', expand=True)
        cols = ("Code", "Name", "CW Total", "Exam", "Total / 160", "%", "Grade")
        self.tree = ttk.Treeview(table_frame, columns=cols, show='headings', selectmode="browse")
        
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')

        for col in cols:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_tree(c, False))
            self.tree.column(col, width=80, anchor="center")
        self.tree.column("Name", width=180, anchor="w")

    # --- Core Logic ---
    def refresh_table(self, data=None):
        for row in self.tree.get_children(): self.tree.delete(row)
        dataset = data if data is not None else self.students
        for s in dataset:
            self.tree.insert("", "end", values=(s.code, s.name, s.total_cw(), s.exam, s.total_score(), f"{s.percentage():.1f}%", s.get_grade_info()))
        self.update_stats()

    def update_stats(self):
        if not self.students:
            self.card_total.config(text="0"); self.card_avg.config(text="0%"); self.card_top.config(text="-")
            return
        total = len(self.students)
        avg = sum(s.percentage() for s in self.students) / total
        top = max(self.students, key=lambda s: s.percentage())
        self.card_total.config(text=str(total))
        self.card_avg.config(text=f"{avg:.1f}%")
        self.card_top.config(text=f"{top.name} ({top.percentage():.1f}%)")

    def update_search(self, *args):
        query = self.search_var.get().lower()
        self.refresh_table([s for s in self.students if query in s.name.lower() or query in str(s.code)])

    def sort_tree(self, col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        try: l.sort(key=lambda t: float(t[0].replace('%', '')), reverse=reverse)
        except: l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l): self.tree.move(k, '', index)
        self.tree.heading(col, command=lambda: self.sort_tree(col, not reverse))

    def show_highest(self):
        if self.students: self.refresh_table([max(self.students, key=lambda s: s.percentage())])

    def show_lowest(self):
        if self.students: self.refresh_table([min(self.students, key=lambda s: s.percentage())])

    # --- ENHANCED FORM LOGIC (Add & Update) ---
    def open_form(self, student=None):
        """Opens a popup window for Adding or Updating a student."""
        form = tk.Toplevel(self.root)
        form.title("Update Student" if student else "Add Student")
        form.geometry("400x500")
        form.configure(bg="white")
        
        # Variables
        v_code = tk.StringVar(value=student.code if student else "")
        v_name = tk.StringVar(value=student.name if student else "")
        v_cw1 = tk.StringVar(value=student.cw[0] if student else "")
        v_cw2 = tk.StringVar(value=student.cw[1] if student else "")
        v_cw3 = tk.StringVar(value=student.cw[2] if student else "")
        v_exam = tk.StringVar(value=student.exam if student else "")

        # Layout Helper
        def add_field(label, var, row):
            tk.Label(form, text=label, font=("Segoe UI", 10, "bold"), bg="white").pack(anchor='w', padx=40, pady=(10, 0))
            tk.Entry(form, textvariable=var, font=("Segoe UI", 10), bg="#f1f5f9").pack(fill='x', padx=40, pady=5)

        add_field("Student Code (1000-9999):", v_code, 0)
        add_field("Student Name:", v_name, 1)
        add_field("Coursework 1 (0-20):", v_cw1, 2)
        add_field("Coursework 2 (0-20):", v_cw2, 3)
        add_field("Coursework 3 (0-20):", v_cw3, 4)
        add_field("Exam Mark (0-100):", v_exam, 5)

        def save_action():
            try:
                # Validation
                code = int(v_code.get())
                if not (1000 <= code <= 9999): raise ValueError("Code must be 4 digits.")
                
                # Check duplicate ID only if adding new
                if not student and any(s.code == code for s in self.students):
                    raise ValueError("Student ID already exists.")

                name = v_name.get().strip()
                if not name: raise ValueError("Name cannot be empty.")

                c1, c2, c3 = int(v_cw1.get()), int(v_cw2.get()), int(v_cw3.get())
                ex = int(v_exam.get())

                if not (0 <= c1 <= 20 and 0 <= c2 <= 20 and 0 <= c3 <= 20):
                    raise ValueError("Coursework marks must be between 0 and 20.")
                if not (0 <= ex <= 100):
                    raise ValueError("Exam mark must be between 0 and 100.")

                # Save Data
                if student: # Update existing
                    student.code, student.name = code, name
                    student.cw, student.exam = [c1, c2, c3], ex
                    messagebox.showinfo("Success", "Record Updated!")
                else: # Add new
                    self.students.append(Student(code, name, c1, c2, c3, ex))
                    messagebox.showinfo("Success", "Student Added!")

                self.save_data()
                self.refresh_table()
                form.destroy()

            except ValueError as ve:
                messagebox.showerror("Invalid Input", str(ve))

        # Save Button
        tk.Button(form, text="Save Record", bg=ACCENT_COLOR, fg="white", font=("Segoe UI", 11, "bold"), 
                  command=save_action).pack(fill='x', padx=40, pady=20)

    def add_student_form(self):
        self.open_form(None)

    def update_student_form(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a student to update.")
            return
        code = int(self.tree.item(selected)['values'][0])
        student = next((s for s in self.students if s.code == code), None)
        if student: self.open_form(student)

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a student to delete.")
            return
        code = int(self.tree.item(selected)['values'][0])
        student = next((s for s in self.students if s.code == code), None)
        
        if student and messagebox.askyesno("Confirm", f"Delete {student.name}?"):
            self.students.remove(student)
            self.save_data()
            self.refresh_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagerApp(root)
    root.mainloop()