from datetime import datetime, timedelta

import dateparser
from assignment import Assignment
import sqlite3
from typing import Optional, List


class AssignmentManager:
    """
    Manages assignments using an SQLite database.
    """

    def __init__(self, db_name="assignments.db"):
        """
        Connects to database and sets up table
        """
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.setup_database()

    def setup_database(self) -> None:
        """
        Creates assignments table
        """
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS assignments (
                name TEXT,
                date TEXT,
                time TEXT,
                done INTEGER
            )"""
        )
        self.conn.commit()

    def add_assignment(self, assignment: Assignment) -> None:
        """
        Adds assignment to the manager
        """
        try:
            with self.conn:
                self.cursor.execute(
                    "INSERT INTO assignments (name, date, time, done) VALUES (?,?,?,?)",
                    (
                        assignment.name,
                        assignment.due_date.strftime("%Y-%m-%d"),
                        assignment.due_time.strftime("%H:%M"),
                        assignment.done,
                    ),
                )
            print(f"{assignment.name} added.")
        except sqlite3.Error as error:
            print(f"Error adding assignment: {error}")

    def remove_assignment(self, assignment_name: str) -> Optional[str]:
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

    def get_assignments(self, weeks_assignments=None) -> List[Assignment]:
        """
        Gets either all assignments, sorted by due date, or assignments that are due within the upcoming week
        """
        try:
            with self.conn:
                if weeks_assignments == True:
                    week_start = datetime.now().date()
                    week_end = datetime.now().date() + timedelta(days=7)
                    self.cursor.execute(
                        "SELECT * FROM assignments WHERE date BETWEEN ? and ? ORDER BY date ASC, time ASC",
                        (week_start, week_end),
                    )
                else:
                    self.cursor.execute(
                        "SELECT * FROM assignments ORDER BY date ASC, time ASC "
                    )
            sorted_assignents = self.cursor.fetchall()
            if not sorted_assignents and weeks_assignments:
                print("No assignments this week!\n")
                return []
            elif not sorted_assignents:
                print("No upcoming assignments!")
                return []
            formatted_assignments = []
            for assignment in sorted_assignents:
                formatted_assignments.append(
                    Assignment(
                        name=assignment[0],
                        due_date=assignment[1],
                        due_time=assignment[2],
                        done=assignment[3],
                    )
                )
            return formatted_assignments
        except sqlite3.Error as error:
            print(f"Error printing assignments: {error}")

    def set_database_field(self, assignment_name: str, field_name: str, field_value: str) -> None:
        """
        Updates specified field of an assignment
        """
        try:
            with self.conn:
                self.cursor.execute(
                    f"UPDATE assignments SET {field_name} = ? WHERE name = ?",
                    (field_value, assignment_name),
                )
        except sqlite3.Error as error:
            print(f"Error changing assignment name: {error}")

    def change_name(self, assignment: Assignment, new_name: str) -> None:
        """
        Changes the name of an assignment
        """
        old_name = assignment.name
        self.set_database_field(old_name, "name", new_name)
        assignment.set_name(new_name)
        print(f"Name for {old_name} changed to {new_name}")

    def change_done(self, assignment: Assignment, done: bool) -> None:
        """
        Set the done state
        """
        self.set_database_field(assignment.name, "done", done)
        assignment.done = done
        print(f"Assignment for {assignment.name} marked as {'done' if done else 'not done'}")

    def change_due_date(self, assignment: Assignment, new_due_date: str) -> None:
        """
        Changes the due date of an assignment
        """
        new_date = (
            dateparser.parse(new_due_date).date().strftime("%Y-%m-%d")
        )  # parse and convert to string
        self.set_database_field(assignment.name, "date", new_date)
        assignment.set_due_date(new_due_date)
        print(f"Due date for {assignment.name} changed to {new_date}.")

    def change_due_time(self, assignment: Assignment, new_due_time: str) -> None:
        """
        Changes the due time of an assignment
        """
        new_time = dateparser.parse(new_due_time).time().strftime("%H:%M")
        self.set_database_field(assignment.name, "time", new_time)
        assignment.set_due_time(new_due_time)
        print(f"Due time for {assignment.name} changed to {new_due_time}.")

    def find_assignment(self, assignment_name: str) -> Optional[Assignment]:
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
                    name=result[0],
                    due_date=result[1],
                    due_time=result[2],
                    done=result[3],
                )
            else:
                return None
        except sqlite3.Error as error:
            print(f"Error finding assignment: {error}")