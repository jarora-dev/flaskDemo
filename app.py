from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Create database connection
conn = sqlite3.connect('students.db', check_same_thread=False)
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS students
             (student_id INTEGER PRIMARY KEY,
             first_name TEXT,
             last_name TEXT,
             dob TEXT,
             amount_due REAL)''')

# Route for creating a new student


@app.route('/students', methods=['POST'])
def create_student():
    try:
        new_student = request.get_json()
        c.execute("INSERT INTO students (first_name, last_name, dob, amount_due) VALUES (?, ?, ?, ?)",
                  (new_student['first_name'], new_student['last_name'], new_student['dob'], new_student['amount_due']))
        conn.commit()
        return jsonify({'message': 'Student created successfully.'})
    except:
        return jsonify({'message': 'An error occurred while creating the student.'}), 500


# Route for getting all students
@app.route('/students', methods=['GET'])
def get_students():
    try:
        c.execute("SELECT * FROM students")
        rows = c.fetchall()
        students = []
        for row in rows:
            student = {'student_id': row[0], 'first_name': row[1],
                       'last_name': row[2], 'dob': row[3], 'amount_due': row[4]}
            students.append(student)
        return jsonify(students)
    except:
        return jsonify({'message': 'An error occurred while getting the students.'}), 500

# Route for getting a specific student


@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    try:
        c.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
        row = c.fetchone()
        if row:
            student = {'student_id': row[0], 'first_name': row[1],
                       'last_name': row[2], 'dob': row[3], 'amount_due': row[4]}
            return jsonify(student)
        else:
            return jsonify({'message': 'Student not found.'}), 404
    except:
        return jsonify({'message': 'An error occurred while getting the student.'}), 500

# Route for updating a student


@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    try:
        updated_student = request.get_json()
        c.execute("UPDATE students SET first_name=?, last_name=?, dob=?, amount_due=? WHERE student_id=?",
                  (updated_student['first_name'], updated_student['last_name'], updated_student['dob'], updated_student['amount_due'], student_id))
        conn.commit()
        c.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
        row = c.fetchone()
        if row:
            student = {'student_id': row[0], 'first_name': row[1],
                       'last_name': row[2], 'dob': row[3], 'amount_due': row[4]}
            return jsonify({'message': 'Student updated successfully.', 'student': student})
        else:
            return jsonify({'message': 'Student not found.'}), 404
    except:
        return jsonify({'message': 'An error occurred while updating the student.'}), 500


# Route for deleting a student
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        c.execute("DELETE FROM students WHERE student_id=?", (student_id,))
        conn.commit()
        return jsonify({'message': 'Student deleted successfully.'})
    except:
        return jsonify({'message': 'An error occurred while deleting the student.'}), 500

# Function to close database connection


@app.teardown_appcontext
def close_connection(exception):
    conn.close()


if __name__ == '__main__':
    app.run(debug=True)
