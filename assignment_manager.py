from datetime import datetime, timedelta
from assignment import Assignment
import sqlite3
import dateparser


class AssignmentManager:
    """
    Manages assignments using an SQLite database.
    """

    def __init__(self, db_name="assignments.db"):
        """
        Connects to database and sets up table
        """
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.setup_database()

    def setup_database(self):
        """
        Creates assignments table
        """
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS assignments (
                name TEXT,
                date TEXT,
                time TEXT
            )"""
        )
        self.conn.commit()

    def add_assignment(self, assignment):
        try:
            with self.conn:
                self.cursor.execute(
                    "INSERT INTO assignments (name, date, time) VALUES (?,?,?)",
                    (
                        assignment.name,
                        assignment.due_date.strftime("%Y-%m-%d"),
                        assignment.due_time.strftime("%H:%M"),
                    ),
                )
            print(f"{assignment.name} added.")
        except sqlite3.Error as error:
            print(f"Error adding assignment: {error}")

    def remove_assignment(self, assignment_name):
        """
        Removes assignment by name from the manager
        """
        try:
            removed = self.find_assignment(assignment_name)
            with self.conn:
                self.cursor.execute(
                    "DELETE from assignments WHERE name = ?", (assignment_name,)
                )
                if self.cursor.rowcount == 1:
                    print(f"{assignment_name} removed.")
                    return removed
                else:
                    print(f"No assignment named {assignment_name}")
                    return None
        except sqlite3.Error as error:
            print(f"Error removing assignment: {error}")

    def print_sorted_assignments(self):
        """
        Prints all assignments, sorted by due date
        """
        try:
            with self.conn:
                self.cursor.execute(
                    "SELECT * FROM assignments ORDER BY date ASC, time ASC "
                )
                sorted_assignments = self.cursor.fetchall()
            if not sorted_assignments:
                print("No upcoming assignments!")
                return
            print("\nUpcoming Assignments:\n")
            for row in sorted_assignments:
                print(f"{row[0]}: Due on {row[1]} at {row[2]}")
        except sqlite3.Error as error:
            print(f"Error printing assignments: {error}")

    def print_weeks_assignments(self):
        """
        Prints assignments that are due within the upcoming week
        """
        try:
            week_start = datetime.now().date()
            week_end = datetime.now().date() + timedelta(days=7)
            with self.conn:
                self.cursor.execute(
                    "SELECT * FROM assignments WHERE date BETWEEN ? and ? ORDER BY date ASC, time ASC",
                    (week_start, week_end),
                )
                sorted_assignments = self.cursor.fetchall()
            if not sorted_assignments:
                print("No assignments this week!\n")
                return
            print("\nUpcoming Week's Assignments:\n")
            for row in sorted_assignments:
                print(f"{row[0]}: Due on {row[1]} at {row[2]}")
        except sqlite3.Error as error:
            print(f"Error printing current week's assignments: {error}")

    def set_database_field(self, field_name, old_field, new_field):
        """
        Updates specified field of an assignment
        """
        try:
            with self.conn:
                self.cursor.execute(
                    "UPDATE assignments SET (%s) = ? WHERE (%s) = ?"
                    % (field_name, field_name),
                    (new_field, old_field),
                )
        except sqlite3.Error as error:
            print(f"Error changing assignment name: {error}")

    def change_name(self, assignment, new_name):
        """
        Changes the name of an assignment
        """
        old_name = assignment.name
        self.set_database_field("name", old_name, new_name)
        assignment.set_name(new_name)
        print(f"Name for {old_name} changed to {new_name}")

    def change_due_date(self, assignment, new_due_date):
        """
        Changes the due date of an assignment
        """
        old_date = assignment.due_date.strftime("%Y-%m-%d")  # convert to string
        new_date = (
            dateparser.parse(new_due_date).date().strftime("%Y-%m-%d")
        )  # parse and convert to string
        self.set_database_field("date", old_date, new_date)
        assignment.set_due_date(new_due_date)
        print(f"Due date for {old_date} changed to {new_date}.")

    def change_due_time(self, assignment, new_due_time):
        """
        Changes the due time of an assignment
        """
        old_time = assignment.due_time.strftime("%H:%M")
        new_time = dateparser.parse(new_due_time).time().strftime("%H:%M")
        self.set_database_field("time", old_time, new_time)
        assignment.set_due_time(new_due_time)
        print(f"Due time for {old_time} changed to {new_due_time}.")

    def find_assignment(self, assignment_name):
        """
        Finds an assignment by name
        """
        try:
            with self.conn:
                self.cursor.execute(
                    "SELECT * FROM assignments WHERE name = ?", (assignment_name,)
                )
                result = self.cursor.fetchone()
            if result:
                return Assignment(
                    name=result[0], due_date=result[1], due_time=result[2]
                )
            else:
                return None
        except sqlite3.Error as error:
            print(f"Error finding assignment: {error}")
