import unittest
from datetime import datetime
from assignment import Assignment
from assignment_manager import AssignmentManager


class TestAssignmentManager(unittest.TestCase):

    def setUp(self):
        """ Creates in-memory database, adds initial assignments"""
        self.assignments = AssignmentManager(":memory:")
        self.assignments.add_assignment(
            Assignment("Science Homework", "2024-07-25", "11:00",done=False)
        )
        self.assignments.add_assignment(
            Assignment("English Homework", "2024-07-19", "8:00",done=False)
        )
        self.test_file = "test_assignments.json"

    def test_add(self):
        """Tests adding an assignment"""
        new_assignment = Assignment("Math Homework", "2024-07-21", "10:00",done=False)
        self.assignments.add_assignment(new_assignment)
        check_assignment = self.assignments.find_assignment("Math Homework")
        self.assertEqual(check_assignment.name, new_assignment.name)
        self.assertEqual(check_assignment.due_date.strftime("%m-%d-%Y"), new_assignment.due_date.strftime("%m-%d-%Y"))
        self.assertEqual(check_assignment.due_time.strftime("%H:%M"), new_assignment.due_time.strftime("%H:%M"))
        
    def test_remove(self):
        """Tests removing an assignment"""
        new_assignment = Assignment("Math Homework", "2024-07-21", "10:00",done=False)
        self.assignments.add_assignment(new_assignment)
        removed_assignment = self.assignments.remove_assignment("Math Homework")
        self.assertEqual(removed_assignment.name, new_assignment.name)
        self.assertEqual(removed_assignment.due_date.strftime("%m-%d-%Y"), new_assignment.due_date.strftime("%m-%d-%Y"))
        self.assertEqual(removed_assignment.due_time.strftime("%H:%M"), new_assignment.due_time.strftime("%H:%M"))
        self.assertIsNone(self.assignments.find_assignment("Math Homework"))
    
    def test_change_name(self):
        """Tests changing an assignment's name"""
        new_name = "French Homework"
        self.assignments.add_assignment(Assignment("Physics Homework", "2024-07-19", "7:00",done=False))
        old_assignment = self.assignments.find_assignment("Physics Homework")
        self.assignments.change_name(old_assignment, new_name)
        updated_assignment = self.assignments.find_assignment(new_name)
        self.assertEqual(updated_assignment.name, new_name)
        self.assertIsNotNone(updated_assignment)

    def test_change_due_date(self):
        """Tests changing an assignment's due date"""
        new_assignment = Assignment("Physics Homework", "2024-07-19", "07:00",done=False)
        self.assignments.add_assignment(new_assignment)
        self.assignments.change_due_date(
            self.assignments.find_assignment("English Homework"), "2024-07-13"
        )
        self.assignments.change_due_date(new_assignment, "2024-07-30")
        self.assertEqual(new_assignment.due_date.strftime("%Y-%m-%d"), "2024-07-30")
        self.assertEqual(
            self.assignments.find_assignment("English Homework").due_date.strftime("%Y-%m-%d"),
            "2024-07-13",
        )

    def test_change_due_time(self):
        """Tests changing an assignment's due time"""
        new_assignment = Assignment("Physics Homework", "2024-07-19", "07:00",done=False)
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
    def test_change_done(self):
        """Tests marking an assignment as done"""
        new_assignment = Assignment("Biology Homework","2024-07-21","10:00",done=False)
        self.assignments.add_assignment(new_assignment)
        self.assignments.change_done(new_assignment,True)
        updated_assignment = self.assignments.find_assignment("Biology Homework")
        self.assertTrue(updated_assignment.done)
        self.assignments.change_done(new_assignment,False)
        updated_assignment = self.assignments.find_assignment("Biology Homework")
        self.assertFalse(updated_assignment.done)
        
if __name__ == "__main__":
    unittest.main()

