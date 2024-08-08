from flask import Flask, request, jsonify, render_template
from assignment import Assignment
from assignment_manager import AssignmentManager

app = Flask(__name__)
manager = AssignmentManager()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/assignments/<string:name>", methods=["GET"])
def view_assignment(name):
    assignment = manager.find_assignment(name)
    if assignment:
        return jsonify(assignment.to_dictionary())
    else:
        return {"Error": "Assignment not found"}, 404


@app.route("/assignments", methods=["GET"])
def view_all_assignments():
    with manager.conn:
        manager.cursor.execute("SELECT * FROM assignments ORDER BY date ASC, time ASC")
        rows = manager.cursor.fetchall()
    assignments = []
    for row in rows:
        assignments.append(
            Assignment(name=row[0], due_date=row[1], due_time=row[2]).to_dictionary()
        )
    return jsonify(assignments)


@app.route("/assignments", methods=["POST"])
def add_assignment():
    if request.is_json:
        json_data = request.get_json()
        new_assignment = Assignment(
            name=json_data["name"],
            due_date=json_data["due_date"],
            due_time=json_data["due_time"],
        )
        manager.add_assignment(new_assignment)
        return (jsonify(new_assignment.to_dictionary()), 201)
    else:
        return {"Error": "Request must be JSON"}, 415


@app.route("/assignments/<string:name>", methods=["DELETE"])
def remove_assignment(name):
    result = manager.remove_assignment(name)
    if result:
        return jsonify(result), 200
    else:
        return {"Error": "Assignment not found"}, 404


@app.route("/assignments/<string:name>", methods=["PATCH"])
def update_assignment(name):
    data = request.get_json()
    new_name = data.get("name")
    new_date = data.get("due_date")
    new_time = data.get("due_time")
    to_update = manager.find_assignment(name)
    if not to_update:
        return {"Error": "Assignment does not exist"}, 404
    if new_name is not None:
        manager.change_name(to_update, new_name)
    if new_date is not None:
        manager.change_due_date(to_update, new_date)
    if new_time is not None:
        manager.change_due_time(to_update, new_time)
    return jsonify(to_update.to_dictionary()), 200


if __name__ == "__main__":
    app.run(debug=True)
