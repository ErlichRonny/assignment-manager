from flask import Flask, request, render_template, redirect, url_for
from assignment import Assignment
from assignment_manager import AssignmentManager
from datetime import datetime
from tabulate import tabulate

app = Flask(__name__)
manager = AssignmentManager()


@app.route("/")
def home():
    weekly_assignments = manager.get_weeks_assignments()
    return render_template("home.html", assignments=weekly_assignments)


@app.route("/add_assignment/")
def add_assignment_page():
    return render_template("add_assignment.html")


@app.route("/success/")
def success_page():
    return render_template("success.html")


@app.route("/view_assignments/")
def view_assignments_page():
    all_assignments = manager.get_sorted_assignments()
    return render_template("view_assignments.html", assignments=all_assignments)


@app.route("/update_assignment/<string:assignment_name>/", methods=["GET"])
def update_assignment_page(assignment_name):
    return render_template("update_assignment.html", name=assignment_name)


@app.route("/assignments/<string:name>", methods=["GET"])
def view_assignment(name):
    assignment = manager.find_assignment(name)
    if assignment:
        pretty = f"Name: {assignment.name}, Due Date: {assignment.due_date}, Due Time: {assignment.due_time}"
        return pretty
    else:
        closest_name = manager.most_similar(name)
        if closest_name:
            to_return = manager.find_assignment(closest_name)
            return f"Closest match ---> Name: {closest_name}, Due Date: {to_return.due_date}, Due Time: {to_return.due_time}"
        else:
            return {"Error": "Assignment not found"}, 404


@app.route("/assignments/", methods=["GET"])
def view_all_assignments():
    with manager.conn:
        manager.cursor.execute("SELECT * FROM assignments ORDER BY date ASC, time ASC")
        rows = manager.cursor.fetchall()
    table = []
    for row in rows:
        table.append([row[0], row[1], row[2]])
    table_printable = tabulate(table, headers=["Name","Due Date","Due Time"],tablefmt="grid")
    return table_printable,{'Content-Type':'text/plain'}


@app.route("/add_assignment/", methods=["POST"])
def add_assignment():
    name = request.form.get("name")
    due_date = request.form.get("due_date")
    due_time = request.form.get("due_time")
    new_assignment = Assignment(name, due_date, due_time)
    if manager.find_assignment(name):
        return {"Error": "Already an assignment with this name"}, 405
    else:
        manager.add_assignment(new_assignment)
        return redirect(url_for("success_page"))
    #TODO: redirection

@app.route("/remove_assignment/<string:name>", methods=["GET"])
def remove_assignment(name):
    result = manager.remove_assignment(name)
    if result is not None:
        return redirect(url_for("view_assignments_page"))
    else:
        return {"Error": "Assignment not found"}, 404


@app.route("/update_assignment/<string:name>", methods=["POST"])
def update_assignment(name):
    new_name = request.form.get("name")
    new_date = request.form.get("due_date")
    new_time = request.form.get("due_time")
    to_update = manager.find_assignment(name)
    
    if not to_update:
        return {"Error": "Assignment does not exist"}, 404
    if new_name:
        manager.change_name(to_update, new_name)
    if new_date:
        manager.change_due_date(to_update, new_date)
    if new_time :
        manager.change_due_time(to_update, new_time)
    return redirect(url_for("success_page"))

if __name__ == "__main__":
    app.run(debug=True)
