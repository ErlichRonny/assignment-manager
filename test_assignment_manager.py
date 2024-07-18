import unittest
from datetime import datetime, timedelta
from assignment import Assignment
from assignment_manager import AssignmentManager
import json
import dateparser


class TestAssignmentManager(unittest.TestCase):

    def setUp(self):
        self.assignments = AssignmentManager()
        self.assignments.add_assignment(
            Assignment("Science Homework", "07-25-2024", "11:00")
        )
        self.assignments.add_assignment(
            Assignment("English Homework", "07-19-2024", "8:00")
        )
        self.test_file = "test_assignments.json"

    def test_add(self):
        """Tests adding an assignment"""
        new_assignment = Assignment("Math Homework", "07-21-2024", "10:00")
        self.assignments.add_assignment(new_assignment)
        check_assignment = self.assignments.find_assignment("Math Homework")
        self.assertEqual(check_assignment.name, new_assignment.name)
        self.assertEqual(check_assignment.due_date, new_assignment.due_date)
        self.assertEqual(check_assignment.due_time, new_assignment.due_time)

    def test_remove(self):
        """Tests removing an assignment"""
        new_assignment = Assignment("Math Homework", "07-21-2024", "10:00")
        self.assignments.add_assignment(new_assignment)
        removed_assignment = self.assignments.remove_assignment("Math Homework")
        self.assignments.remove_assignment("Science Homework")
        self.assertIsNone(self.assignments.find_assignment("Math Homework"))
        self.assertIsNone(self.assignments.find_assignment("Science Homework"))
        self.assertEqual(removed_assignment.name, new_assignment.name)
        self.assertEqual(removed_assignment.due_date, new_assignment.due_date)
        self.assertEqual(removed_assignment.due_time, new_assignment.due_time)

    def test_change_name(self):
        """Tests changing an assignment name"""
        new_assignment = Assignment("Physics Homework", "07-19-2024", "07:00")
        self.assignments.change_name(
            self.assignments.find_assignment("English Homework"), "Spanish Homework"
        )
        self.assignments.change_name(new_assignment, "French Homework")
        self.assertEqual(new_assignment.name, "French Homework")
        self.assertEqual(
            self.assignments.find_assignment("English Homework").name,
            "Spanish Homework",
        )

    def test_change_due_date(self):
        """Tests changing an assignment due date"""
        new_assignment = Assignment("Physics Homework", "07-19-2024", "07:00")
        self.assignments.change_due_date(
            self.assignments.find_assignment("English Homework"), "07-13-2024"
        )
        self.assignments.change_due_date(new_assignment, "07-30-2024")
        self.assertEqual(new_assignment.due_date.strftime("%m-%d-%Y"), "07-30-2024")
        self.assertEqual(
            self.assignments.find_assignment("English Homework").due_date.strftime(
                "%m-%d-%Y"
            ),
            "07-13-2024",
        )

    def test_change_due_time(self):
        """Tests changing an assignment due time"""
        new_assignment = Assignment("Physics Homework", "07-19-2024", "07:00")
        self.assignments.change_due_time(
            self.assignments.find_assignment("English Homework"), "11:59"
        )
        self.assignments.change_due_time(new_assignment, "01:30")
        self.assertEqual(new_assignment.due_time.strftime("%H:%M"), "01:30")
        self.assertEqual(
            self.assignments.find_assignment("English Homework").due_time.strftime(
                "%H:%M"
            ),
            "11:59",
        )

    def test_save_to_json(self):
        """Tests saving assignments to a JSON file"""
        new_assignment = Assignment("Physics Homework", "07-19-2024", "07:00")
        self.assignments.add_assignment(new_assignment)
        self.assignments.save_to_json(self.test_file)
        with open(self.test_file, "r") as json_file:
            data = json.load(json_file)
        self.assertIn("Physics Homework", data)
        self.assertEqual(data["Physics Homework"]["name"], "Physics Homework")
        self.assertEqual(data["Physics Homework"]["due_date"], "2024-07-19")
        self.assertEqual(data["Physics Homework"]["due_time"], "07:00")

    def test_load_json(self):
        """Tests loading assignments from a JSON file"""
        new_assignment = Assignment("Physics Homework", "07-19-2024", "07:00")
        self.assignments.add_assignment(new_assignment)
        self.assignments.save_to_json(self.test_file)
        self.assignments.load_from_json(self.test_file)
        loaded_assignment = self.assignments.find_assignment("Physics Homework")
        self.assertIsNotNone(loaded_assignment)
        self.assertEqual(loaded_assignment.name, new_assignment.name)
        self.assertEqual(loaded_assignment.due_date, new_assignment.due_date)
        self.assertEqual(loaded_assignment.due_time, new_assignment.due_time)


if __name__ == "__main__":
    unittest.main()
