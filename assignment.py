from datetime import datetime, timedelta


class Assignment:

    def __init__(self, name, due_date_input, due_time_input):
        self.name = name
        self.due_date = datetime.strptime(due_date_input, "%m/%d/%y").date() # Parse due date
        self.due_time = datetime.strptime(due_time_input, "%I:%M %p").time() # Parse due time

    def get_due(self):
        return datetime.combine(self.due_date, self.due_time) # Combine date and time to datetime object

    def get_due_str(self):
        # Format due date/time as string
        return f"Due on {self.due_date.strftime('%a, %m/%d/%y')} at {self.due_time.strftime('%I:%M %p')}" 

    def set_name(self, new_name):
        self.name = new_name
        
    def set_due_date(self, new_due_date):
        self.due_date = datetime.strptime(new_due_date, "%m/%d/%y").date() # Parse due date

    def set_due_time(self, new_due_time):
        self.due_time = datetime.strptime(new_due_time, "%I:%M %p").time() # Parse due time

    def days_until_due(self):
        current_date = datetime.now().date() # Gets current date
        return f"{(self.due_date-current_date).days} days until {self.name} is due" # Calculate days until due date


class AssignmentManager:
    def __init__(self):
        self.assignments = []

    def add_assignment(self, assignment):
        self.assignments.append(assignment)
        print(f"{assignment.name} added.")

    def remove_assignment(self, assignment_name):
        assignment = self.find_assignment(assignment_name)
        if assignment:
            self.assignments.remove(assignment)
            print(f"{assignment_name} removed.")
        else:
            print(f"No assignment named {assignment_name}")

    def get_sorted_assignments(self):
        sorted_assignments = sorted(self.assignments, key=lambda x: x.get_due()) # Sort assignments by due date
        print("\nUpcoming Assignments:\n")
        for assignment in sorted_assignments:
            print(f"{assignment.name}: {assignment.get_due_str()}")
        if not sorted_assignments:
            print("No upcoming assignments!")

    def get_weeks_assignments(self):
        sorted_assignments = sorted(self.assignments, key=lambda x: x.get_due()) # Sort assignments by due date
        week_end = datetime.now().date() + timedelta(days=7) # Calculate 1 week from now
        week_assignments = []
        print("\nUpcoming Week's Assignments:\n")
        for assignment in sorted_assignments:
            if datetime.now().date() <= assignment.due_date <= week_end: # If within week, add assignment to week_assignments
                week_assignments.append(assignment)
                print(f"{assignment.name}: {assignment.get_due_str()}")
        if not week_assignments:
            print("No assignments this week!\n")

    def change_name(self, assignment, new_name):
        old_name = assignment.name
        assignment.set_name(new_name)
        print(f"Name for {old_name} changed to {new_name}.")
            
    def change_due_date(self, assignment, new_due_date):
        old_date = assignment.due_date
        assignment.set_due_date(new_due_date)
        print(f"Due date for {old_date} changed to {new_due_date}.")
        
    def change_due_time(self, assignment, new_due_time):
        old_time = assignment.due_time
        assignment.set_due_time(new_due_time)
        print(f"Due time for {old_time} changed to {new_due_time}.")
        
    def find_assignment(self, assignment_name):
        for assignment in self.assignments:
            if assignment_name == assignment.name:
                return assignment
        return None
    
def main():
    tracker = AssignmentManager()

    while True:
        print(
            "\n 1. Add Assignment\n 2. Delete Assignment\n 3. Modify Assignment \n 4. Sort by Due Date\n 5. View the week's assignments\n 6. Quit\n"
        )
        choice = input("What would you like to do? ")
        choice = int(choice)
        if choice == 1:
            name = input("Give this assignment a name: ")
            due_date = input("When is it due? (In the format MM/DD/YY): ")
            due_time = input("What time is it due? (In the format HH:MM AM/PM): ")
            tracker.add_assignment(Assignment(name, due_date, due_time))
        elif choice == 2:
            tracker.get_sorted_assignments()
            to_remove = input("Which assignment would you like to delete? ")
            tracker.remove_assignment(to_remove)
        elif choice == 3:
            modify = input(" 1. Change Name\n 2. Change Due Date\n 3. Change Due Time ")
            tracker.get_sorted_assignments()
            assignment_name = input("Which assignment do you want to change? ")
            assignment = tracker.find_assignment(assignment_name)
            if assignment:
                modify = int(modify)
                if modify == 1:
                    new_name = input("New assignment name? ")
                    tracker.change_name(assignment, new_name)
                elif modify == 2:
                    new_date = input("New due date? (In the format MM/DD/YY): ")
                    tracker.change_due_date(assignment, new_date)
                elif modify == 3:
                    new_time = input("New due time? (In the format HH:MM AM/PM): ")
                    tracker.change_due_time(assignment, new_time)
                else:
                    print("Invalid input: please enter 1, 2, or 3. \n")  
            else:
                print(f"No assignment named {assignment_name}")
        elif choice == 4:
            tracker.get_sorted_assignments()
        elif choice == 5:
            tracker.get_weeks_assignments()
        elif choice == 6:
            break
        else:
            print("Invalid input: please enter a number between 1 and 5. \n")

if __name__ == "__main__":
    main()