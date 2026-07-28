# Student Assignment Submission Portal

## Project Overview

The Student Assignment Submission Portal is a web-based application developed using Flask, MySQL, HTML, and CSS. The system allows teachers to create assignments and students to submit their work online. All assignment and submission data are stored in a MySQL database.

---

## Technologies Used

- Python
- Flask
- MySQL
- HTML
- CSS
- AWS EC2
- Linux (Amazon Linux 2023)

---

## Project Structure

```
studentportal/
│
├── app.py
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── student.html
│   ├── teacher.html
│   ├── assignments.html
│   ├── create_assignment.html
│   ├── uploadassignment.html
│   ├── submissions.html
│
├── static/
│   └── style.css
│
└── uploads/
```

---

# File Descriptions

## 1. app.py

Purpose:
Main Flask application file.

Functions:
- Connects Flask with MySQL database.
- Handles Login and Registration.
- Controls Teacher Dashboard.
- Controls Student Dashboard.
- Creates Assignments.
- Uploads Assignment Files.
- Displays Student Submissions.
- Manages User Sessions.
- Routes all pages.

Main Routes:
- /
- /login
- /register
- /student
- /teacher
- /assignments
- /create_assignment
- /uploadassignment
- /submissions
- /logout

---

## 2. login.html

Purpose:
User Login Page.

Features:
- Username input
- Password input
- Login button
- Redirects users according to role
- Teacher login
- Student login

---

## 3. register.html

Purpose:
New User Registration Page.

Features:
- Username registration
- Password creation
- Role selection
  - Student
  - Teacher
- Stores user details in MySQL database

---

## 4. student.html

Purpose:
Student Dashboard.

Features:
- View Assignments
- Upload Assignment
- View My Submissions
- Logout

Modules:
- Assignments
- Upload Assignment
- My Submissions

---

## 5. teacher.html

Purpose:
Teacher Dashboard.

Features:
- Create Assignment
- View Assignments
- View Student Submissions
- Logout

Modules:
- Create Assignment
- View Assignments
- Student Submissions

---

## 6. assignments.html

Purpose:
Display available assignments.

Features:
- Assignment Title
- Description
- Due Date
- Teacher Name
- Assignment List

Used By:
- Teachers
- Students

---

## 7. create_assignment.html

Purpose:
Create New Assignments.

Features:
- Assignment Title
- Assignment Description
- Due Date
- Submit Button

Database:
Stores assignment information in the assignments table.

---

## 8. uploadassignment.html

Purpose:
Student Assignment Upload Page.

Features:
- Select Assignment
- Upload PDF File
- Submit Assignment

Process:
1. Student selects file.
2. File stored in uploads folder.
3. Submission record saved in MySQL database.

---

## 9. submissions.html

Purpose:
Display Submitted Assignments.

Features:
- Student Name
- Assignment Name
- File Name
- Submission Date
- Download/View File

Used By:
- Students
- Teachers

---

## Database Tables

### users

Stores login information.

Columns:
- id
- username
- password
- role

---

### assignments

Stores assignment details.

Columns:
- id
- title
- description
- due_date
- teacher_name

---

### submissions

Stores uploaded assignments.

Columns:
- id
- student_name
- assignment_id
- file_name
- submission_date

---

## Project Workflow

### Teacher

1. Login
2. Create Assignment
3. View Assignments
4. View Student Submissions

### Student

1. Register/Login
2. View Assignments
3. Upload Assignment
4. View Submitted Assignments

---

## AWS Deployment

Services Used:

### EC2
Hosts Flask Application.

### MySQL
Stores Users, Assignments and Submission Data.

### Security Group

Open:
- Port 22 (SSH)
- Port 80 (HTTP)

---

## Future Enhancements

- File Download Feature
- Assignment Deadline Validation
- Email Notifications
- S3 File Storage
- Teacher Feedback System
- Marks and Grading System

---

## Author

Student Assignment Submission Portal

Developed using Flask, MySQL, HTML, CSS and AWS EC2.