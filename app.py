import os
from flask import Flask, request, render_template, flash, jsonify, Response
from assignment import Assignment
from assignment_manager import AssignmentManager
from datetime import datetime
from dotenv import load_dotenv

load_dotenv() # Loads environment variables from .env
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")  # Required for flash messages
manager = AssignmentManager()

@app.route("/")
def home() -> str:
    """ 
    Renders home page
    """
    all_assignments = manager.get_assignments()
    return render_template("view_assignments.html", assignments=all_assignments)

@app.route("/add_assignment/", methods=["POST"])
def add_assignment() -> Response:
    """ 
    Adds a new assignment, flashes success or failure messages
    """
    name = request.form.get("name")
    due_date = request.form.get("due_date")
    due_time = request.form.get("due_time")
    new_assignment = Assignment(name, due_date, due_time, False)
    # Check if assignment with same name already exists
    if manager.find_assignment(name):
        flash("Assignment with this name already exists!", "danger")
        return jsonify(success=False)

    manager.add_assignment(new_assignment)
    flash("Assignment added successfully!", "success")
    return jsonify(success=True)

@app.route("/remove_assignment/<string:name>", methods=["GET"])
def remove_assignment(name: str) -> Response:
    """
    Removes assignment by name, flashes success or failure messages
    """
    result = manager.remove_assignment(name)
    if result is None:
        flash("Assignment not found!", "danger")
        return jsonify(success=False)    
    
    flash("Assignment removed successfully!", "success")
    return jsonify(success=True)

@app.route("/set_done/<string:name>/<int:state>", methods=["GET"])
def set_done(name: str, state: int) -> Response:
    """ 
    Sets assignment as done or not done
    """
    result = manager.change_done(manager.find_assignment(name), state)
    return jsonify(success=True)
        
@app.route("/update_assignment/<string:name>", methods=["POST"])
def update_assignment(name: str) -> Response:
    """
    Updates an assignment's name, due date, or due time depending 
    on form data
    """
    new_name = request.form.get("name")
    new_date = request.form.get("due_date")
    new_time = request.form.get("due_time")
    to_update = manager.find_assignment(name)
    
    if not to_update:
        flash("Assignment does not exist!", "danger")
        return jsonify(success=False)
        
    if new_name:
        manager.change_name(to_update, new_name)
    if new_date:
        manager.change_due_date(to_update, new_date)
    if new_time :
        manager.change_due_time(to_update, new_time)
    flash("Assignment edited successfully!", "success")
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)
