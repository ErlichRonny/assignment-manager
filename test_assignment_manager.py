import unittest
from datetime import datetime, timedelta
from assignment import Assignment
from assignment_manager import AssignmentManager


class TestAssignmentManager(unittest.TestCase):

    def setUp(self):
        self.assignments = AssignmentManager(":memory:")
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
        new_name = "French Homework"
        self.assignments.add_assignment(Assignment("Physics Homework", "07-19-2024", "7:00"))
        old_assignment = self.assignments.find_assignment("Physics Homework")
        self.assignments.change_name(old_assignment, new_name)
        updated_assignment = self.assignments.find_assignment(new_name)
        self.assertEqual(updated_assignment.name, new_name)

    def test_change_due_date(self):
        """Tests changing an assignment due date"""
        new_assignment = Assignment("Physics Homework", "07-19-2024", "07:00")
        self.assignments.add_assignment(new_assignment)
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
        self.assignments.add_assignment(new_assignment)
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
        
if __name__ == "__main__":
    unittest.main()

