"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    project_grade = hackbright.get_grades_by_github(github)
    html = render_template('student_info.html', 
                                    first=first,
                                    last=last,
                                    github=github,
                                    project_grade=project_grade)
    return html 

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""
    return render_template("student_search.html")

@app.route('/project')
def get_project():
    """Show information about a project"""
    title = request.args.get('title')
    title, description, max_grade  = hackbright.get_project_by_title(title)
    student_grades = hackbright.get_grades_by_title(title)
    
    return render_template("project.html", 
                            title=title,
                            description=description,
                            max_grade=max_grade,
                            student_grades = student_grades)

@app.route("/homepage")
def display_students_and_projects():
    students = hackbright.get_all_students()
    return render_template("homepage.html",
                            students = students)

@app.route("/add-student")
def get_add_student_form():
    """Show form for searching for a student."""
    return render_template("add_student.html")

@app.route("/new-student", methods=['POST'])
def make_new_student():
    first = request.form.get('first')
    last = request.form.get('last')
    github = request.form.get('github')
    hackbright.make_new_student(first, last, github)
    return render_template('new-student.html',
                            first=first,
                            last=last,
                            github=github)
if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
