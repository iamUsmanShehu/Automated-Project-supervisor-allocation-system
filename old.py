import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# MySQL connection setup
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="project_allocation"
    )

# Data insertion functions
def insert_student(name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (name) VALUES (%s)', (name,))
    conn.commit()
    conn.close()

def insert_supervisor(name, expertise, availability):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO supervisors (name, expertise, availability) VALUES (%s, %s, %s)', (name, expertise, availability))
    conn.commit()
    conn.close()

def insert_project(title, student_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO projects (title, student_id) VALUES (%s, %s)', (title, student_id))
    conn.commit()
    conn.close()

def allocate_supervisors():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT id, expertise FROM supervisors WHERE availability > 0')
    supervisors = cursor.fetchall()

    cursor.execute('SELECT id, title FROM projects WHERE supervisor_id IS NULL')
    projects = cursor.fetchall()

    allocation = {}
    for project in projects:
        for supervisor in supervisors:
            allocation[project[0]] = supervisor[0]
            cursor.execute('UPDATE projects SET supervisor_id = %s WHERE id = %s', (supervisor[0], project[0]))
            cursor.execute('UPDATE supervisors SET availability = availability - 1 WHERE id = %s', (supervisor[0],))
            break
    conn.commit()
    conn.close()
    return allocation

def get_statistics():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM students')
    total_students = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM supervisors')
    total_supervisors = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM projects WHERE supervisor_id IS NOT NULL')
    allocated_projects = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM projects WHERE supervisor_id IS NULL')
    unallocated_projects = cursor.fetchone()[0]

    conn.close()

    return total_students, total_supervisors, allocated_projects, unallocated_projects

def search_projects(title, offset=0, limit=10):
    conn = create_connection()
    cursor = conn.cursor()
    if title:
        cursor.execute('SELECT * FROM projects WHERE title LIKE %s LIMIT %s OFFSET %s', ('%' + title + '%', limit, offset))
    else:
        cursor.execute('SELECT * FROM projects LIMIT %s OFFSET %s', (limit, offset))
    results = cursor.fetchall()

    cursor.execute('SELECT COUNT(*) FROM projects WHERE title LIKE %s', ('%' + title + '%',) if title else ('%',))
    total_projects = cursor.fetchone()[0]

    conn.close()
    return results, total_projects

# Tkinter GUI
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Supervisor Allocation")

        # Notebook (tab manager)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill="both")

        # Tabs
        self.create_dashboard_tab()
        self.create_student_tab()
        self.create_supervisor_tab()
        self.create_project_tab()

        # Set the dashboard as the default tab
        self.notebook.select(self.dashboard_tab)

    def create_student_tab(self):
        self.student_tab = Frame(self.notebook)
        self.notebook.add(self.student_tab, text="Add Student")

        self.student_name = StringVar()
        Label(self.student_tab, text="Student Name:").grid(row=0, column=0)
        Entry(self.student_tab, textvariable=self.student_name).grid(row=0, column=1)
        Button(self.student_tab, text="Add Student", command=self.add_student).grid(row=0, column=2)

    def create_supervisor_tab(self):
        self.supervisor_tab = Frame(self.notebook)
        self.notebook.add(self.supervisor_tab, text="Add Supervisor")

        self.supervisor_name = StringVar()
        self.supervisor_expertise = StringVar()
        self.supervisor_availability = IntVar()

        Label(self.supervisor_tab, text="Supervisor Name:").grid(row=0, column=0)
        Entry(self.supervisor_tab, textvariable=self.supervisor_name).grid(row=0, column=1)
        Label(self.supervisor_tab, text="Expertise:").grid(row=1, column=0)
        Entry(self.supervisor_tab, textvariable=self.supervisor_expertise).grid(row=1, column=1)
        Label(self.supervisor_tab, text="Availability:").grid(row=2, column=0)
        Entry(self.supervisor_tab, textvariable=self.supervisor_availability).grid(row=2, column=1)
        Button(self.supervisor_tab, text="Add Supervisor", command=self.add_supervisor).grid(row=3, column=1)

    def create_project_tab(self):
        self.project_tab = Frame(self.notebook)
        self.notebook.add(self.project_tab, text="Add Project")

        self.project_title = StringVar()
        self.project_student_id = IntVar()

        Label(self.project_tab, text="Project Title:").grid(row=0, column=0)
        Entry(self.project_tab, textvariable=self.project_title).grid(row=0, column=1)
        Label(self.project_tab, text="Student ID:").grid(row=1, column=0)
        Entry(self.project_tab, textvariable=self.project_student_id).grid(row=1, column=1)
        Button(self.project_tab, text="Add Project", command=self.add_project).grid(row=2, column=1)

    def create_dashboard_tab(self):
        self.dashboard_tab = Frame(self.notebook)
        self.notebook.add(self.dashboard_tab, text="Dashboard")

        self.stats_frame = Frame(self.dashboard_tab)
        self.stats_frame.pack(pady=10)

        self.total_students_label = Label(self.stats_frame, text="Total Students: 0")
        self.total_students_label.grid(row=0, column=0, padx=10)

        self.total_supervisors_label = Label(self.stats_frame, text="Total Supervisors: 0")
        self.total_supervisors_label.grid(row=0, column=1, padx=10)

        self.allocated_projects_label = Label(self.stats_frame, text="Allocated Projects: 0")
        self.allocated_projects_label.grid(row=0, column=2, padx=10)

        self.unallocated_projects_label = Label(self.stats_frame, text="Unallocated Projects: 0")
        self.unallocated_projects_label.grid(row=0, column=3, padx=10)

        Button(self.stats_frame, text="Allocate Supervisors", command=self.allocate_supervisors).grid(row=1, column=1, columnspan=2, pady=10)

        self.search_frame = Frame(self.dashboard_tab)
        self.search_frame.pack(pady=10)

        self.search_query = StringVar()
        Label(self.search_frame, text="Search Projects:").grid(row=0, column=0)
        Entry(self.search_frame, textvariable=self.search_query).grid(row=0, column=1)
        Button(self.search_frame, text="Search", command=self.search_projects).grid(row=0, column=2)

        self.search_results = ttk.Treeview(self.dashboard_tab, columns=("ID", "Title", "Student ID", "Supervisor ID"), show='headings')
        self.search_results.heading("ID", text="ID")
        self.search_results.heading("Title", text="Title")
        self.search_results.heading("Student ID", text="Student ID")
        self.search_results.heading("Supervisor ID", text="Supervisor ID")
        self.search_results.pack(fill="both", expand=True)

        self.pagination_frame = Frame(self.dashboard_tab)
        self.pagination_frame.pack(pady=10)

        self.current_page = 0
        self.results_per_page = 10

        self.prev_button = Button(self.pagination_frame, text="Previous", command=self.prev_page)
        self.prev_button.grid(row=0, column=0)

        self.next_button = Button(self.pagination_frame, text="Next", command=self.next_page)
        self.next_button.grid(row=0, column=1)

        self.update_statistics()
        self.search_projects()

    def add_student(self):
        insert_student(self.student_name.get())
        messagebox.showinfo("Info", "Student added successfully")
        self.update_statistics()

    def add_supervisor(self):
        insert_supervisor(self.supervisor_name.get(), self.supervisor_expertise.get(), self.supervisor_availability.get())
        messagebox.showinfo("Info", "Supervisor added successfully")
        self.update_statistics()

    def add_project(self):
        insert_project(self.project_title.get(), self.project_student_id.get())
        messagebox.showinfo("Info", "Project added successfully")
        self.update_statistics()

    def allocate_supervisors(self):
        allocation = allocate_supervisors()
        messagebox.showinfo("Allocation", f"Allocation Completed: {allocation}")
        self.update_statistics()

    def update_statistics(self):
        total_students, total_supervisors, allocated_projects, unallocated_projects = get_statistics()
        self.total_students_label.config(text=f"Total Students: {total_students}")
        self.total_supervisors_label.config(text=f"Total Supervisors: {total_supervisors}")
        self.allocated_projects_label.config(text=f"Allocated Projects: {allocated_projects}")
        self.unallocated_projects_label.config(text=f"Unallocated Projects: {unallocated_projects}")

    def search_projects(self):
        for row in self.search_results.get_children():
            self.search_results.delete(row)
        results, total_projects = search_projects(self.search_query.get(), self.current_page * self.results_per_page, self.results_per_page)
        for result in results:
            self.search_results.insert('', 'end', values=result)
        self.update_pagination_buttons(total_projects)

    def update_pagination_buttons(self, total_projects):
        if self.current_page == 0:
            self.prev_button.config(state=DISABLED)
        else:
            self.prev_button.config(state=NORMAL)
        if (self.current_page + 1) * self.results_per_page >= total_projects:
            self.next_button.config(state=DISABLED)
        else:
            self.next_button.config(state=NORMAL)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.search_projects()

    def next_page(self):
        self.current_page += 1
        self.search_projects()

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
