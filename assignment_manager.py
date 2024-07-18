from datetime import datetime, timedelta
from assignment import Assignment
import json


class AssignmentManager:
    """
    Manages a dictionary of assignments
    """

    def __init__(self):
        """
        Initializes empty dictionary to manage assignments
        """
        self.assignments = {}

    def add_assignment(self, assignment):
        """
        Adds a new assignment to the manager
        """
        self.assignments[assignment.name] = assignment
        print(f"{assignment.name} added.")

    def remove_assignment(self, assignment_name):
        """
        Removes assignment by name from the manager
        """
        if assignment_name in self.assignments:
            removed = self.assignments[assignment_name]
            del self.assignments[assignment_name]
            print(f"{assignment_name} removed.")
            return removed
        else:
            print(f"No assignment named {assignment_name}")

    def print_sorted_assignments(self):
        """
        Prints all assignments, sorted by due date
        """
        sorted_assignments = sorted(
            self.assignments.values(), key=lambda x: x.get_due()
        )  # Sort assignments by due date
        print("\nUpcoming Assignments:\n")
        if not sorted_assignments:
            print("No upcoming assignments!")
        for assignment in sorted_assignments:
            print(f"{assignment.name}: {assignment.get_due_str()}")

    def print_weeks_assignments(self):
        """
        Prints assignments that are due within the upcoming week
        """
        sorted_assignments = sorted(
            self.assignments.values(), key=lambda x: x.get_due()
        )  # Sort assignments by due date
        week_end = datetime.now().date() + timedelta(
            days=7
        )  # Calculate 1 week from now
        week_assignments = []
        print("\nUpcoming Week's Assignments:\n")

        for assignment in sorted_assignments:
            if (
                datetime.now().date() <= assignment.due_date <= week_end
            ):  # If within week, add assignment to week_assignments
                week_assignments.append(assignment)
                print(f"{assignment.name}: {assignment.get_due_str()}")
        if not week_assignments:
            print("No assignments this week!\n")

    def change_name(self, assignment, new_name):
        """
        Changes the name of an assignment
        """
        old_name = assignment.name
        assignment.set_name(new_name)
        print(f"Name for {old_name} changed to {new_name}.")

    def change_due_date(self, assignment, new_due_date):
        """
        Changes the due date of an assignment
        """
        old_date = assignment.due_date
        assignment.set_due_date(new_due_date)
        print(f"Due date for {old_date} changed to {new_due_date}.")

    def change_due_time(self, assignment, new_due_time):
        """
        Changes the due time of an assignment
        """
        old_time = assignment.due_time
        assignment.set_due_time(new_due_time)
        print(f"Due time for {old_time} changed to {new_due_time}.")

    def find_assignment(self, assignment_name):
        """
        Finds an assignment by name
        """
        return self.assignments.get(assignment_name, None)

    def save_to_json(self, filename):
        assignments_dict = {}
        for assignment in self.assignments.values():
            assignments_dict[assignment.name] = assignment.to_dictionary()
        try:
            with open(filename, "w") as f:
                json.dump(assignments_dict, f, indent=2)
        except TypeError:
            print("There was an error with serializing the assignments.")
        except IOError:
            print(f"There was an error with saving to {filename}.")

    def load_from_json(self, saved_assignments):
        try:
            with open("saved_assignments.json", "r") as json_file:
                data = json.load(json_file)
                for assignment_dict in data.values():
                    assignment = Assignment(
                        assignment_dict["name"],
                        assignment_dict["due_date"],
                        assignment_dict["due_time"],
                    )
                    self.assignments[assignment.name] = assignment
        except FileNotFoundError:
            print("This file was not found.")
        except json.JSONDecodeError:
            print("This file has invalid JSON data.")
