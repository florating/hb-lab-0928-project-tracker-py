"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///project-tracker'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def get_student_by_github(github):
    """Given a GitHub account name, print info about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM students
        WHERE github = :github
        """

    db_cursor = db.session.execute(QUERY, {'github': github})

    row = db_cursor.fetchone()

    print(f"Student: {row[0]} {row[1]}\nGitHub account: {row[2]}")


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """
    
    QUERY = """ 
        INSERT INTO students (first_name, last_name, github)
        VALUES (:first_name, :last_name, :github)
        """

    db.session.execute(QUERY, {'first_name': first_name, 'last_name': last_name, 'github': github})
    db.session.commit()
    print(f"Successfully added student: {first_name} {last_name}")


def get_project_by_title(title):
    """Given a project title, print information about the project."""

    QUERY = """
        SELECT *
        FROM projects WHERE title = :title
        """
    db_cursor = db.session.execute(QUERY, {'title': title})
    row = db_cursor.fetchone()
    print(f"Project Title: {row[1]} \nProject Description: {row[2]} \nMax Grade: {row[3]}")


def get_grade_by_github_title(github, title):
    """Print grade student received for a project.
    SELECT grade FROM grades WHERE student_github = 'jhacks' AND project_title = 'Blockly';
    """
    QUERY = """
        SELECT grade FROM grades WHERE student_github = :github AND project_title = :title
        """
    db_cursor = db.session.execute(QUERY, {'github': github, 'title': title})
    row = db_cursor.fetchone()
    print(f"Grade: {row[0]}")


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    # check if student in grades table
    # if student not in grades table
        # check if student in students table
        # if student is in students table:
            # get the first_name and last_name from the students table given github
            # INSERT INTO grades table
            # assign_grade
        # if student is not in students table
            # print error statment: no such student
    # if student in grades table
        # do the things below

    QUERY = """
        UPDATE grades SET grade = :grade
        WHERE student_github = :github AND project_title = :title
        """
    
    db.session.execute(QUERY, {'github': github, 'title': title, 'grade': grade})

    db.session.commit()

    print(f"Successfully assigned a grade of {grade} for project {title}")


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received
    as a command.
    """

    command = None

    while command != "quit":
        input_string = input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args  # unpack!
            make_new_student(first_name, last_name, github)
        elif command == "project_by_title":
            title = args[0]
            get_project_by_title(title)
        elif command == "grade_by_github_title":
            github, title = args
            get_grade_by_github_title(github, title)
        elif command == "assign_grade":
            github, title, grade = args
            assign_grade(github, title, grade)
        else:
            if command != "quit":
                print("Invalid Entry. Try again.")


if __name__ == "__main__":
    connect_to_db(app)

    handle_input()

    # To be tidy, we close our database connection -- though,
    # since this is where our program ends, we'd quit anyway.

    db.session.close()
