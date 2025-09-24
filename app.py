from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

students = {}
teachers = {}
courses = {}

# ==== Models (in-memory) ====

class Student:
    def __init__(self, name):
        self.name = name
        self.courses = {}

class Teacher:
    def __init__(self, name):
        self.name = name
        self.courses = []

class Course:
    def __init__(self, name):
        self.name = name
        self.teacher = None
        self.students = []

# ==== Routes ====

@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.json
    name = data['name']
    if name in students:
        return jsonify({"error": "Student already exists"}), 400
    students[name] = Student(name)
    return jsonify({"message": f"Student {name} added"})

@app.route('/add_teacher', methods=['POST'])
def add_teacher():
    data = request.json
    name = data['name']
    if name in teachers:
        return jsonify({"error": "Teacher already exists"}), 400
    teachers[name] = Teacher(name)
    return jsonify({"message": f"Teacher {name} added"})

@app.route('/add_course', methods=['POST'])
def add_course():
    data = request.json
    name = data['name']
    if name in courses:
        return jsonify({"error": "Course already exists"}), 400
    courses[name] = Course(name)
    return jsonify({"message": f"Course {name} added"})

@app.route('/assign_teacher', methods=['POST'])
def assign_teacher():
    data = request.json
    course_name = data['course']
    teacher_name = data['teacher']

    if course_name not in courses or teacher_name not in teachers:
        return jsonify({"error": "Invalid course or teacher"}), 400

    course = courses[course_name]
    teacher = teachers[teacher_name]

    course.teacher = teacher
    teacher.courses.append(course)
    return jsonify({"message": f"Assigned {teacher_name} to {course_name}"})


@app.route('/enroll', methods=['POST'])
def enroll():
    data = request.json
    student_name = data['student']
    course_name = data['course']

    if student_name not in students or course_name not in courses:
        return jsonify({"error": "Invalid student or course"}), 400

    student = students[student_name]
    course = courses[course_name]

    student.courses[course_name] = None
    course.students.append(student)
    return jsonify({"message": f"{student_name} enrolled in {course_name}"})


@app.route('/grade', methods=['POST'])
def grade():
    data = request.json
    teacher_name = data['teacher']
    student_name = data['student']
    course_name = data['course']
    grade = data['grade']

    if teacher_name not in teachers or student_name not in students or course_name not in courses:
        return jsonify({"error": "Invalid teacher, student, or course"}), 400

    teacher = teachers[teacher_name]
    student = students[student_name]
    course = courses[course_name]

    if course not in teacher.courses:
        return jsonify({"error": "Teacher does not teach this course"}), 403

    student.courses[course_name] = grade
    return jsonify({"message": f"{student_name} graded {grade} in {course_name}"})


@app.route('/students', methods=['GET'])
def get_students():
    result = []
    for s in students.values():
        result.append({
            "name": s.name,
            "courses": s.courses
        })
    return jsonify(result)


@app.route('/courses', methods=['GET'])
def get_courses():
    result = []
    for c in courses.values():
        result.append({
            "name": c.name,
            "teacher": c.teacher.name if c.teacher else None,
            "students": [s.name for s in c.students]
        })
    return jsonify(result)

# ==== Run ====
if __name__ == '__main__':
    app.run(debug=True)
