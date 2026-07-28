from flask import Flask, render_template, request, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pymysql
import os

app = Flask(__name__)
app.secret_key = "studentportal_secret_key"

# =========================
# UPLOAD FOLDER
# =========================

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {
    'pdf',
    'ppt',
    'pptx',
    'doc',
    'docx',
    'jpg',
    'jpeg',
    'png'
}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    """Return True if filename has a permitted extension."""
    if '.' not in filename:
        return False
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS


# =========================
# DATABASE CONNECTION
# =========================

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="studentadmin",
        password="student123",
        database="studentportal",
        cursorclass=pymysql.cursors.DictCursor
    )

# =========================
# HOME PAGE
# =========================

@app.route('/')
def home():
    return redirect('/login')

# =========================
# REGISTRATION
# =========================

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        if not username or not email or not password or not role:
            flash("All fields are required", "error")
            return redirect('/register')

        hashed_password = generate_password_hash(password)

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
            INSERT INTO users
            (username, email, password, role)
            VALUES (%s,%s,%s,%s)
            """,
            (username, email, hashed_password, role))

            conn.commit()
            flash("Registration Successful!", "success")

        except pymysql.err.IntegrityError:
            flash("Username or email already exists", "error")

        finally:
            conn.close()

        return redirect('/login')

    return render_template('register.html')

# =========================
# LOGIN
# =========================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM users
        WHERE username=%s
        """,
        (username,))

        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user['password'], password):

            role = user['role']

            if role.lower() == "teacher":
                return redirect('/teacher')

            if role.lower() == "student":
                return redirect('/student')

        flash("Invalid Username or Password", "error")

    return render_template('login.html')

# =========================
# STUDENT DASHBOARD
# =========================

@app.route('/student')
def dashboard():
    return render_template('student.html')

# =========================
# TEACHER DASHBOARD
# =========================

@app.route('/teacher')
def teacher():
    return render_template('teacher.html')

# =========================
# CREATE ASSIGNMENT
# =========================

@app.route('/create_assignment', methods=['GET', 'POST'])
def create_assignment():

    if request.method == 'POST':

        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']

        file = request.files.get('file')

        filename = ""

        if file and file.filename != "":

            if allowed_file(file.filename):

                filename = secure_filename(file.filename)

                file.save(
                    os.path.join(
                        app.config['UPLOAD_FOLDER'],
                        filename
                    )
                )

            else:
                flash("File type not allowed", "error")
                return redirect('/create_assignment')

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO assignments
        (
            title,
            description,
            due_date,
            filename
        )
        VALUES (%s,%s,%s,%s)
        """,
        (
            title,
            description,
            due_date,
            filename
        ))

        conn.commit()
        conn.close()

        flash(
            "Assignment Created Successfully!",
            "success"
        )

        return redirect('/assignments')

    return render_template('create_assignment.html')

# =========================
# VIEW ASSIGNMENTS
# =========================

@app.route('/assignments')
def assignments():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        title,
        description,
        due_date,
        filename
    FROM assignments
    ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return render_template(
        'assignment.html',
        assignments=data
    )

# =========================
# OPEN ASSIGNMENT FILE
# =========================

@app.route('/assignment_file/<filename>')
def assignment_file(filename):

    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        secure_filename(filename)
    )

# =========================
# STUDENT UPLOAD
# =========================

@app.route('/uploads', methods=['GET', 'POST'])
def upload():

    if request.method == 'POST':

        student_name = request.form['student_name']
        assignment_title = request.form['assignment_title']

        file = request.files.get('file')

        if not file or file.filename == "":

            flash(
                "Please Select a File",
                "error"
            )

            return redirect('/uploads')

        if not allowed_file(file.filename):
            flash("File type not allowed", "error")
            return redirect('/uploads')

        filename = secure_filename(file.filename)

        file.save(
            os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )
        )

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO submissions
        (
            student_name,
            assignment_title,
            filename
        )
        VALUES (%s,%s,%s)
        """,
        (
            student_name,
            assignment_title,
            filename
        ))

        conn.commit()
        conn.close()

        flash(
            "Assignment Submitted Successfully!",
            "success"
        )

        return redirect('/submissions')

    return render_template('uploadassignment.html')

# =========================
# VIEW SUBMISSIONS
# =========================

@app.route('/submissions')
def submissions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        student_name,
        assignment_title,
        filename,
        submission_date
    FROM submissions
    ORDER BY submission_date DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return render_template(
        'submission.html',
        submissions=data
    )

# =========================
# DOWNLOAD SUBMITTED FILE
# =========================

@app.route('/submission_file/<filename>')
def submission_file(filename):

    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        secure_filename(filename)
    )

# =========================
# LOGOUT
# =========================

@app.route('/logout')
def logout():

    flash(
        "Logged Out Successfully!",
        "success"
    )

    return redirect('/login')

# =========================
# RUN APP
# =========================

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
