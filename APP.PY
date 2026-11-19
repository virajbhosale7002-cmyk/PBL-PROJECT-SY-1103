from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import get_db_connection

app = Flask(__name__)
app.secret_key = "replace-this-with-a-private-secret-key"


def admin_required():
    return "user_id" in session and session.get("user_role") == "admin"


def role_required(role):
    return "user_id" in session and session.get("user_role") == role


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "")

        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)

        cur.execute(
            "SELECT id,name,email,role FROM users "
            "WHERE email=%s AND password=%s AND role=%s",
            (email, password, role)
        )

        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            session.update(
                user_id=user["id"],
                name=user["name"],
                email=user["email"],
                user_role=user["role"]
            )
            return redirect(url_for("dashboard"))

        flash("Invalid email, password or role.")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    role = session.get("user_role")

    if role == "admin":
        return redirect(url_for("admin_dashboard"))
    if role == "mentor":
        return redirect(url_for("mentor_dashboard"))
    if role == "mentee":
        return redirect(url_for("mentee_dashboard"))
    if role == "parent":
        return redirect(url_for("parent_dashboard"))

    return redirect(url_for("logout"))


@app.route("/admin-dashboard")
def admin_dashboard():
    if not admin_required():
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    counts = {}

    for key, table in [
        ("Students", "students"),
        ("Faculty", "faculty"),
        ("Subjects", "subjects"),
        ("Classes", "classes")
    ]:
        cur.execute(f"SELECT COUNT(*) AS total FROM {table}")
        counts[key] = cur.fetchone()["total"]

    cur.close()
    conn.close()

    return render_template(
        "dashboard.html",
        title="Admin Dashboard",
        counts=counts
    )


@app.route("/mentor-dashboard")
def mentor_dashboard():
    if not role_required("mentor"):
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        title="Mentor Dashboard",
        counts={}
    )


@app.route("/mentee-dashboard")
def mentee_dashboard():
    if not role_required("mentee"):
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        title="Mentee Dashboard",
        counts={}
    )


@app.route("/parent-dashboard")
def parent_dashboard():
    if not role_required("parent"):
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        title="Parent Dashboard",
        counts={}
    )


@app.route("/admin/faculty")
def admin_faculty():
    if not admin_required():
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        "SELECT f.id,u.name,u.email,f.employee_id,f.designation,"
        "f.joining_date,d.department_name FROM faculty f "
        "JOIN users u ON f.user_id=u.id "
        "LEFT JOIN departments d ON f.department_id=d.id "
        "ORDER BY f.id DESC"
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return render_template(
        "listing.html",
        title="Faculty",
        rows=rows
    )


@app.route("/admin/students")
def admin_students():
    if not admin_required():
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        "SELECT s.id,u.name,u.email,s.enrollment_number,"
        "s.roll_number,c.class_name FROM students s "
        "JOIN users u ON s.user_id=u.id "
        "LEFT JOIN classes c ON s.class_id=c.id "
        "ORDER BY s.id DESC"
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return render_template(
        "listing.html",
        title="Students",
        rows=rows
    )


@app.route("/admin/announcements")
def admin_announcements():
    if not admin_required():
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM announcements ORDER BY id DESC")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "listing.html",
        title="Announcements",
        rows=rows
    )


@app.route("/admin/subjects")
def admin_subjects():
    if not admin_required():
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM subjects ORDER BY id DESC")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "listing.html",
        title="Subjects",
        rows=rows
    )


@app.route("/my-mentees")
def my_mentees():
    if not role_required("mentor"):
        return redirect(url_for("login"))

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute(
        "SELECT s.id,u.name,u.email,s.enrollment_number,"
        "s.roll_number,c.class_name FROM students s "
        "JOIN users u ON s.user_id=u.id "
        "LEFT JOIN classes c ON s.class_id=c.id "
        "JOIN mentor_mentees mm ON mm.student_id=s.id "
        "JOIN faculty f ON f.id=mm.faculty_id "
        "WHERE f.user_id=%s",
        (session["user_id"],)
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return render_template(
        "listing.html",
        title="My Mentees",
        rows=rows
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
