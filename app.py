from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from assignment import Assignment
from assignment_manager import AssignmentManager
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'testing123'  # Required for flash messages
manager = AssignmentManager()

@app.route("/")
def home():
    all_assignments = manager.get_assignments()
    return render_template("view_assignments.html", assignments=all_assignments)

@app.route("/add_assignment/", methods=["POST"])
def add_assignment():
    name = request.form.get("name")
    due_date = request.form.get("due_date")
    due_time = request.form.get("due_time")
    new_assignment = Assignment(name, due_date, due_time)
    if manager.find_assignment(name):
        flash("Assignment with this name already exists!", "danger")
        return jsonify(sucess=False)

    manager.add_assignment(new_assignment)
    flash("Assignment added successfully!", "success")
    return jsonify(sucess=True)

@app.route("/remove_assignment/<string:name>", methods=["GET"])
def remove_assignment(name):
    result = manager.remove_assignment(name)
    if result is None:
        flash("Assignment not found!", "danger")
        return jsonify(sucess=False)    
    flash("Assignment removed successfully!", "success")
    return jsonify(sucess=True)
        
@app.route("/update_assignment/<string:name>", methods=["POST"])
def update_assignment(name):
    new_name = request.form.get("name")
    new_date = request.form.get("due_date")
    new_time = request.form.get("due_time")
    to_update = manager.find_assignment(name)
    
    if not to_update:
        flash("Assignment does not exist!", "danger")
        return jsonify(sucess=False)
        
    if new_name:
        manager.change_name(to_update, new_name)
    if new_date:
        manager.change_due_date(to_update, new_date)
    if new_time :
        manager.change_due_time(to_update, new_time)
    flash("Assignment edited successfully!", "success")
    return jsonify(sucess=True)

if __name__ == "__main__":
    app.run(debug=True)
