from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

# Configure SQLite database (you can use PostgreSQL/MySQL instead)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Define Task Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    done = db.Column(db.Boolean, default=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Task Resource for CRUD operations
class TaskResource(Resource):
    def get(self, task_id):
        task = Task.query.get_or_404(task_id)
        return {"id": task.id, "title": task.title, "description": task.description, "done": task.done}

    def put(self, task_id):
        task = Task.query.get_or_404(task_id)
        data = request.get_json()
        task.title = data.get("title", task.title)
        task.description = data.get("description", task.description)
        task.done = data.get("done", task.done)
        db.session.commit()
        return {"message": "Task updated successfully"}

    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return {"message": "Task deleted successfully"}, 200

# Task List Resource for GET (all tasks) and POST (create task)
class TaskListResource(Resource):
    def get(self):
        tasks = Task.query.all()
        return [{"id": task.id, "title": task.title, "description": task.description, "done": task.done} for task in tasks]

    def post(self):
        data = request.get_json()
        if "title" not in data:
            return {"error": "Title is required"}, 400
        new_task = Task(title=data["title"], description=data.get("description", ""), done=data.get("done", False))
        db.session.add(new_task)
        db.session.commit()
        return {"message": "Task created", "id": new_task.id}, 201

# Add resource routes
api.add_resource(TaskListResource, "/tasks")
api.add_resource(TaskResource, "/tasks/<int:task_id>")

if __name__ == "__main__":
    app.run(debug=True)
