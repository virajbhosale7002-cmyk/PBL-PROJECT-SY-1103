
CREATE DATABASE IF NOT EXISTS mentor_mentee_db;
USE mentor_mentee_db;
CREATE TABLE IF NOT EXISTS users (
id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(120) NOT NULL,
email VARCHAR(160) UNIQUE NOT NULL, password VARCHAR(255) NOT NULL,
role ENUM('admin','mentor','mentee','parent') NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS departments (
id INT AUTO_INCREMENT PRIMARY KEY, department_name VARCHAR(120) NOT NULL,
department_code VARCHAR(30), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS courses (
id INT AUTO_INCREMENT PRIMARY KEY, department_id INT,
course_name VARCHAR(120) NOT NULL, course_code VARCHAR(30), duration_years INT,
FOREIGN KEY (department_id) REFERENCES departments(id)
);
CREATE TABLE IF NOT EXISTS classes (
id INT AUTO_INCREMENT PRIMARY KEY, course_id INT,
academic_year VARCHAR(20), semester INT, division VARCHAR(10), class_name VARCHAR(80),
FOREIGN KEY (course_id) REFERENCES courses(id)
);
CREATE TABLE IF NOT EXISTS faculty (
id INT AUTO_INCREMENT PRIMARY KEY, user_id INT UNIQUE, department_id INT,
employee_id VARCHAR(50), designation VARCHAR(80), joining_date DATE,
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
FOREIGN KEY (department_id) REFERENCES departments(id)
);
CREATE TABLE IF NOT EXISTS students (
id INT AUTO_INCREMENT PRIMARY KEY, user_id INT UNIQUE, class_id INT,
roll_number VARCHAR(30), enrollment_number VARCHAR(80) UNIQUE, admission_year VARCHAR(20),
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
FOREIGN KEY (class_id) REFERENCES classes(id)
);
CREATE TABLE IF NOT EXISTS subjects (
id INT AUTO_INCREMENT PRIMARY KEY, course_id INT, subject_name VARCHAR(120) NOT NULL,
subject_code VARCHAR(30), credits INT DEFAULT 0, semester INT,
FOREIGN KEY (course_id) REFERENCES courses(id)
);
CREATE TABLE IF NOT EXISTS faculty_subjects (
id INT AUTO_INCREMENT PRIMARY KEY, faculty_id INT NOT NULL, subject_id INT NOT NULL,
class_id INT NOT NULL, academic_year VARCHAR(20) NOT NULL, semester INT NOT NULL,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (faculty_id) REFERENCES faculty(id) ON DELETE CASCADE,
FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
UNIQUE (faculty_id,subject_id,class_id,academic_year,semester)
);
CREATE TABLE IF NOT EXISTS mentor_mentees (
id INT AUTO_INCREMENT PRIMARY KEY, faculty_id INT NOT NULL, student_id INT NOT NULL,
assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (faculty_id) REFERENCES faculty(id) ON DELETE CASCADE,
FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
UNIQUE(faculty_id,student_id)
);
CREATE TABLE IF NOT EXISTS parent_students (
id INT AUTO_INCREMENT PRIMARY KEY, parent_user_id INT NOT NULL, student_id INT NOT NULL,
relationship VARCHAR(50),
FOREIGN KEY (parent_user_id) REFERENCES users(id) ON DELETE CASCADE,
FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS announcements (
id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(200) NOT NULL, message TEXT,
created_by INT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (created_by) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS meetings (
id INT AUTO_INCREMENT PRIMARY KEY, mentor_id INT, student_id INT, meeting_date DATETIME,
topic VARCHAR(255), notes TEXT, status VARCHAR(30) DEFAULT 'scheduled',
FOREIGN KEY (mentor_id) REFERENCES faculty(id), FOREIGN KEY (student_id) REFERENCES students(id)
);
CREATE TABLE IF NOT EXISTS tasks (
id INT AUTO_INCREMENT PRIMARY KEY, mentor_id INT, student_id INT, title VARCHAR(200),
description TEXT, due_date DATE, status VARCHAR(30) DEFAULT 'pending',
FOREIGN KEY (mentor_id) REFERENCES faculty(id), FOREIGN KEY (student_id) REFERENCES students(id)
);
CREATE TABLE IF NOT EXISTS notifications (
Mentor–Mentee Management System — Source Code Page 9
id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, message TEXT,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, is_read BOOLEAN DEFAULT FALSE,
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
