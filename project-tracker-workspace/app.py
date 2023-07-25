from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from database import engine_conn_string

# import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = engine_conn_string()
app.config[
    "SECRET_KEY"
] = "ca290e3692d7cee6efd34dc8c5c621b557af981f8e0c1e4be1e911c6d58b5b2d"

db = SQLAlchemy()


# Define a route
@app.route("/")
def show_projects():
    return render_template("index.html")


@app.route("/project/<project_id>")
def show_tasks(project_id):
    return render_template("project-tasks.html", project_id=project_id)


@app.route("/add/project", methods=["POST"])
def add_project():
    # TODO: Add project
    return "Project added successfully"


@app.route("/add/task/<project_id>", methods=["POST"])
def add_task(project_id):
    # TODO: Add task
    return "Task added successfully"


app.run(debug=True)
