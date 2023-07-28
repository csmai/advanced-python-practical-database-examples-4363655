from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from database import engine_conn_string

app = Flask(__name__)

# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = engine_conn_string()
app.config[
    "SECRET_KEY"
] = "ca290e3692d7cee6efd34dc8c5c621b557af981f8e0c1e4be1e911c6d58b5b2d"

db = SQLAlchemy(app)


class Project(db.Model):
    __tablename__ = "projects"

    project_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=50))


class Task(db.Model):
    __tablename__ = "tasks"

    task_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey(Project.project_id))
    description = db.Column(db.String(length=50))

    project = db.relationship("Project")


print("This is a printed message.")


# Define a route
@app.route("/")
def show_projects():
    return render_template("index.html", projects=Project.query.all())


@app.route("/project/<project_id>")
def show_tasks(project_id):
    app.logger.error(Task.query.filter_by(project_id=project_id).all())
    return render_template(
        "project-tasks.html",
        project=Project.query.filter_by(project_id=project_id).first(),
        tasks=Task.query.filter_by(project_id=project_id).all(),
    )


@app.route("/add/project", methods=["POST"])
def add_project():
    if request.form["project-title"]:
        new_project = Project(title=request.form["project-title"])
        db.session.add(new_project)
        db.session.commit()
        flash("Project added successfully", "message")
    else:
        flash("Please enter a project title!", "error")
    return redirect(url_for("show_projects"))


@app.route("/add/task/<project_id>", methods=["POST"])
def add_task(project_id):
    if request.form["task-name"]:
        new_task = Task(description=request.form["task-name"], project_id=project_id)
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully", "message")
    else:
        flash("Please enter task description!", "error")
    return redirect(url_for("show_tasks", project_id=project_id))


@app.route("/delete/task/<project_id>/<task_id>", methods=["POST"])
def delete_task(project_id, task_id):
    task_to_del = Task.query.filter_by(project_id=project_id, task_id=task_id).first()
    db.session.delete(task_to_del)
    db.session.commit()
    flash("Task deleted successfully", "message")
    return redirect(url_for("show_tasks", project_id=project_id))


@app.route("/delete/project/<project_id>", methods=["POST"])
def delete_project(project_id):
    proj_to_del = Project.query.filter_by(project_id=project_id).first()
    tasks_to_del = Task.query.filter_by(project_id=project_id).all()
    if tasks_to_del:
        for task in tasks_to_del:
            delete_task(project_id, task.task_id)
            print(f"deleted: {task.description}")
    print(tasks_to_del, type(tasks_to_del))
    db.session.delete(proj_to_del)
    db.session.commit()
    flash("Project deleted successfully", "message")

    return redirect(url_for("show_projects", project_id=project_id))


app.run(debug=True)
