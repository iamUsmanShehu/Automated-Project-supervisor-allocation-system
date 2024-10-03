import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="project_allocation"
    )

def get_supervisors():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, discipline, availability FROM supervisors')
    supervisors = cursor.fetchall()
    conn.close()
    return supervisors

def get_supervisor_id_by_name(name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM supervisors WHERE name = %s', (name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_students_with_supervisor_names():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT students.id, students.name, students.ug_number, students.cgpa, supervisors.name
        FROM students
        JOIN supervisors ON students.supervisor_id = supervisors.id
    ''')
    students = cursor.fetchall()
    conn.close()
    return students

def get_students_by_supervisor(supervisor_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT students.id, students.name, students.ug_number, students.cgpa, supervisors.name
        FROM students
        JOIN supervisors ON students.supervisor_id = supervisors.id
        WHERE students.supervisor_id = %s
    ''', (supervisor_id,))
    students = cursor.fetchall()
    conn.close()
    return students

def student_exists(ug_number):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM students WHERE ug_number = %s', (ug_number,))
    exists = cursor.fetchone()[0]
    conn.close()
    return exists > 0

def insert_student(name, ug_number, cgpa, supervisor_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (name, ug_number, cgpa, supervisor_id) VALUES (%s, %s, %s, %s)', (name, ug_number, cgpa, supervisor_id))
    conn.commit()
    conn.close()

def insert_supervisor(name, discipline, availability):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO supervisors (name, discipline, availability) VALUES (%s, %s, %s)', (name, discipline, availability))
    conn.commit()
    conn.close()

def update_supervisor(supervisor_id, name, discipline, availability):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE supervisors SET name = %s, discipline = %s, availability = %s WHERE id = %s', (name, discipline, availability, supervisor_id))
    conn.commit()
    conn.close()

def delete_supervisor(supervisor_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM supervisors WHERE id = %s', (supervisor_id,))
    conn.commit()
    conn.close()

def get_statistics():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM students')
    total_students = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM supervisors')
    total_supervisors = cursor.fetchone()[0]
    conn.close()
    return total_students, total_supervisors
