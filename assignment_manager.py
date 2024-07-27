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
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            self.setup_database()
        except sqlite3.Error as error:
            print(f"Connection error: {error}")

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
            if self.cursor.rowcount > 0:
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
            print("\nUpcoming Assignments:\n")
            if not sorted_assignments:
                print("No upcoming assignments!")
            for row in sorted_assignments:
                assignment = Assignment(name=row[0], due_date=row[1], due_time=row[2])
                print(f"{assignment.name}: {assignment.get_due_str()}")
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
            print("\nUpcoming Week's Assignments:\n")
            if not sorted_assignments:
                print("No assignments this week!\n")
            for row in sorted_assignments:
                assignment = Assignment(name=row[0], due_date=row[1], due_time=row[2])
                print(f"{assignment.name}: {assignment.get_due_str()}")
        except sqlite3.Error as error:
            print(f"Error printing current week's assignments: {error}")

    def change_name(self, assignment, new_name):
        """
        Changes the name of an assignment
        """
        try:
            old_name = assignment.name
            with self.conn:
                self.cursor.execute(
                    "UPDATE assignments SET name = ? WHERE name = ?", (new_name, old_name)
                )
            assignment.set_name(new_name)
            print(f"Name for {old_name} changed to {new_name}")

            print(f"Name for {old_name} changed to {new_name}.")
        except sqlite3.Error as error:
            print(f"Error changing assignment name: {error}")
            
    def change_due_date(self, assignment, new_due_date):
        """
        Changes the due date of an assignment
        """
        try:
            old_date = assignment.due_date.strftime("%Y-%m-%d")  # convert to string
            new_date = (
                dateparser.parse(new_due_date).date().strftime("%Y-%m-%d")
            )  # parse and convert to string
            with self.conn:
                self.cursor.execute(
                    "UPDATE assignments SET date = ? WHERE date = ?",
                    (new_date, old_date),
                )
            assignment.set_due_date(new_due_date)
            print(f"Due date for {old_date} changed to {new_date}.")
        except sqlite3.Error as error:
            print(f"Error changing assignment due date: {error}")

    def change_due_time(self, assignment, new_due_time):
        """
        Changes the due time of an assignment
        """
        try:
            old_time = assignment.due_time.strftime("%H:%M")
            new_time = dateparser.parse(new_due_time).time().strftime("%H:%M")
            with self.conn:
                self.cursor.execute(
                    "UPDATE assignments SET time = ? WHERE time = ?",
                    (new_time, old_time),
                )
            assignment.set_due_time(new_due_time)
            print(f"Due time for {old_time} changed to {new_due_time}.")
        except sqlite3.Error as error:
            print(f"Error changing assignment due time: {error}")
            
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
                return Assignment(name=result[0], due_date=result[1], due_time=result[2])
            else:
                print(f"No assignment named {assignment_name} found.")
                return None
        except sqlite3.Error as error:
            print(f"Error finding assignment: {error}")