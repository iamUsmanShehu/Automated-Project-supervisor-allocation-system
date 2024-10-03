from tkinter import *
from tkinter import ttk, messagebox
import database as db

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Supervisor Allocation System - By Danfillo")

        # Notebook (tab manager)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill="both")

        # Tabs
        self.create_dashboard_tab()
        self.create_student_tab()
        self.create_supervisor_tab()
        self.create_student_under_supervisor_tab()

        # Set the dashboard as the default tab
        self.notebook.select(self.dashboard_tab)

    def create_student_tab(self):
        self.student_tab = Frame(self.notebook)
        self.notebook.add(self.student_tab, text="Add Student")

        self.student_name = StringVar()
        self.student_ug_number = StringVar()
        self.student_cgpa = DoubleVar()
        self.student_supervisor = StringVar()

        Label(self.student_tab, text="Student Name:").grid(row=0, column=0)
        Entry(self.student_tab, textvariable=self.student_name).grid(row=0, column=1)
        Label(self.student_tab, text="UG Number:").grid(row=1, column=0)
        Entry(self.student_tab, textvariable=self.student_ug_number).grid(row=1, column=1)
        Label(self.student_tab, text="CGPA:").grid(row=2, column=0)
        Entry(self.student_tab, textvariable=self.student_cgpa).grid(row=2, column=1)
        Label(self.student_tab, text="Supervisor:").grid(row=3, column=0)
        self.supervisor_options = ttk.Combobox(self.student_tab, textvariable=self.student_supervisor)
        self.supervisor_options.grid(row=3, column=1)
        self.load_supervisors()
        Button(self.student_tab, text="Save Student", command=self.add_student).grid(row=4, column=1)

        # Student table
        self.student_table = ttk.Treeview(self.student_tab, columns=("ID", "Name", "UG Number", "CGPA", "Supervisor"), show='headings')
        self.student_table.heading("ID", text="ID")
        self.student_table.heading("Name", text="Name")
        self.student_table.heading("UG Number", text="UG Number")
        self.student_table.heading("CGPA", text="CGPA")
        self.student_table.heading("Supervisor", text="Supervisor")
        self.student_table.grid(row=5, columnspan=2)

        self.load_students()

    def load_students(self):
        for row in self.student_table.get_children():
            self.student_table.delete(row)
        students = db.get_students_with_supervisor_names()
        for student in students:
            self.student_table.insert('', 'end', values=student)

    def load_supervisors(self):
        supervisors = db.get_supervisors()
        self.supervisor_options['values'] = [supervisor[1] for supervisor in supervisors]

    def add_student(self):
        name = self.student_name.get()
        ug_number = self.student_ug_number.get()
        cgpa = self.student_cgpa.get()
        supervisor_name = self.student_supervisor.get()

        if not (name and ug_number and cgpa and supervisor_name):
            messagebox.showerror("Error", "All fields are required")
            return

        if db.student_exists(ug_number):
            messagebox.showerror("Error", "Student with this UG Number already exists")
            return

        supervisor_id = db.get_supervisor_id_by_name(supervisor_name)
        db.insert_student(name, ug_number, cgpa, supervisor_id)
        messagebox.showinfo("Success", "Student added successfully")
        self.load_students()

    def create_supervisor_tab(self):
        self.supervisor_tab = Frame(self.notebook)
        self.notebook.add(self.supervisor_tab, text="Add Supervisor")

        self.supervisor_name = StringVar()
        self.supervisor_discipline = StringVar()
        self.supervisor_availability = IntVar()

        Label(self.supervisor_tab, text="Supervisor Name:").grid(row=0, column=0)
        Entry(self.supervisor_tab, textvariable=self.supervisor_name).grid(row=0, column=1)
        Label(self.supervisor_tab, text="Discipline:").grid(row=1, column=0)
        Entry(self.supervisor_tab, textvariable=self.supervisor_discipline).grid(row=1, column=1)
        Label(self.supervisor_tab, text="Availability:").grid(row=2, column=0)
        Entry(self.supervisor_tab, textvariable=self.supervisor_availability).grid(row=2, column=1)
        Button(self.supervisor_tab, text="Add Supervisor", command=self.add_supervisor).grid(row=3, column=1)

        # Supervisor table
        self.supervisor_table = ttk.Treeview(self.supervisor_tab, columns=("ID", "Name", "Discipline", "Availability"), show='headings')
        self.supervisor_table.heading("ID", text="ID")
        self.supervisor_table.heading("Name", text="Name")
        self.supervisor_table.heading("Discipline", text="Discipline")
        self.supervisor_table.heading("Availability", text="Availability")
        self.supervisor_table.grid(row=4, columnspan=2)

        self.load_supervisors_table()

        # CRUD Buttons
        self.edit_button = Button(self.supervisor_tab, text="Edit", command=self.edit_supervisor)
        self.edit_button.grid(row=5, column=0, pady=10)
        self.delete_button = Button(self.supervisor_tab, text="Delete", command=self.delete_supervisor)
        self.delete_button.grid(row=5, column=1, pady=10)

    def load_supervisors_table(self):
        for row in self.supervisor_table.get_children():
            self.supervisor_table.delete(row)
        supervisors = db.get_supervisors()
        for supervisor in supervisors:
            self.supervisor_table.insert('', 'end', values=supervisor)

    def add_supervisor(self):
        name = self.supervisor_name.get()
        discipline = self.supervisor_discipline.get()
        availability = self.supervisor_availability.get()

        if not (name and discipline and availability):
            messagebox.showerror("Error", "All fields are required")
            return

        db.insert_supervisor(name, discipline, availability)
        messagebox.showinfo("Success", "Supervisor added successfully")
        self.load_supervisors_table()

    def edit_supervisor(self):
        selected_item = self.supervisor_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No supervisor selected")
            return

        item = self.supervisor_table.item(selected_item)
        supervisor_id = item['values'][0]
        name = item['values'][1]
        discipline = item['values'][2]
        availability = item['values'][3]

        edit_window = Toplevel(self.root)
        edit_window.title("Edit Supervisor")

        new_name = StringVar(edit_window, value=name)
        new_discipline = StringVar(edit_window, value=discipline)
        new_availability = IntVar(edit_window, value=availability)

        Label(edit_window, text="Supervisor Name:").grid(row=0, column=0)
        Entry(edit_window, textvariable=new_name).grid(row=0, column=1)
        Label(edit_window, text="Discipline:").grid(row=1, column=0)
        Entry(edit_window, textvariable=new_discipline).grid(row=1, column=1)
        Label(edit_window, text="Availability:").grid(row=2, column=0)
        Entry(edit_window, textvariable=new_availability).grid(row=2, column=1)

        def save_changes():
            db.update_supervisor(supervisor_id, new_name.get(), new_discipline.get(), new_availability.get())
            messagebox.showinfo("Success", "Supervisor updated successfully")
            self.load_supervisors_table()
            edit_window.destroy()

        Button(edit_window, text="Save", command=save_changes).grid(row=3, column=1)

    def delete_supervisor(self):
        selected_item = self.supervisor_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No supervisor selected")
            return

        item = self.supervisor_table.item(selected_item)
        supervisor_id = item['values'][0]

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this supervisor?")
        if confirm:
            db.delete_supervisor(supervisor_id)
            messagebox.showinfo("Success", "Supervisor deleted successfully")
            self.load_supervisors_table()

    def create_dashboard_tab(self):
        self.dashboard_tab = Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text="Dashboard")

        self.stats_frame = Frame(self.dashboard_tab)
        self.stats_frame.pack(pady=10)

        self.total_students_label = Label(self.stats_frame, text="Total Students: 0")
        self.total_students_label.grid(row=0, column=0, padx=10)

        self.total_supervisors_label = Label(self.stats_frame, text="Total Supervisors: 0")
        self.total_supervisors_label.grid(row=0, column=1, padx=10)

        self.refresh_button = Button(self.stats_frame, text="Refresh Stats", command=self.update_dashboard_stats)
        self.refresh_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.update_dashboard_stats()

    def create_student_under_supervisor_tab(self):
        self.student_under_supervisor_tab = Frame(self.notebook)
        self.notebook.add(self.student_under_supervisor_tab, text="Students Under Supervisor")

        self.supervisor_list = ttk.Combobox(self.student_under_supervisor_tab)
        self.supervisor_list.grid(row=0, column=0, padx=10, pady=10)
        self.supervisor_list.bind("<<ComboboxSelected>>", self.load_students_by_supervisor)

        # Student table
        self.student_under_supervisor_table = ttk.Treeview(self.student_under_supervisor_tab, columns=("ID", "Name", "UG Number", "CGPA", "Supervisor"), show='headings')
        self.student_under_supervisor_table.heading("ID", text="ID")
        self.student_under_supervisor_table.heading("Name", text="Name")
        self.student_under_supervisor_table.heading("UG Number", text="UG Number")
        self.student_under_supervisor_table.heading("CGPA", text="CGPA")
        self.student_under_supervisor_table.heading("Supervisor", text="Supervisor")
        self.student_under_supervisor_table.grid(row=1, columnspan=2)

        self.load_supervisors_for_student_tab()

    def load_supervisors_for_student_tab(self):
        supervisors = db.get_supervisors()
        self.supervisor_list['values'] = [supervisor[1] for supervisor in supervisors]

    def load_students_by_supervisor(self, event=None):
        supervisor_name = self.supervisor_list.get()
        supervisor_id = db.get_supervisor_id_by_name(supervisor_name)
        students = db.get_students_by_supervisor(supervisor_id)
        self.update_student_table(self.student_under_supervisor_table, students)

    def update_student_table(self, table, data):
        for row in table.get_children():
            table.delete(row)
        for student in data:
            table.insert('', 'end', values=student)

    def update_dashboard_stats(self):
        total_students, total_supervisors = db.get_statistics()
        self.total_students_label.config(text=f"Total Students: {total_students}")
        self.total_supervisors_label.config(text=f"Total Supervisors: {total_supervisors}")

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
