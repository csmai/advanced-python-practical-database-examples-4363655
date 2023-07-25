from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from database import engine_conn_string

app = Flask(__name__)

app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = engine_conn_string()
app.config[
    "SECRET_KEY"
] = "ca290e3692d7cee6efd34dc8c5c621b557af981f8e0c1e4be1e911c6d58b5b2d"

db = SQLAlchemy(app)


class Project(db.Model):
    __tablename__ = "projects"

    project_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=50))


print("This is a printed message.")


# Define a route
@app.route("/")
def show_projects():
    print("Project.query.all()")
    app.logger.error(Project.query.all())
    app.logger.error(Project.query.all()[0].project_id)
    return render_template("index.html", projects=Project.query.all())


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
