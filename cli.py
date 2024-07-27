from assignment import Assignment
from assignment_manager import AssignmentManager


def main():
    """
    Runs command-line interface to manage assignments
    """
    tracker = AssignmentManager()

    while True:
        print(
            "\n 1. Add Assignment\n 2. Delete Assignment\n 3. Modify Assignment \n 4. Sort by Due Date\n 5. View the week's assignments\n 6. Quit\n"
        )
        choice = input("What would you like to do? ")
        try:
            choice = int(choice)
        except ValueError:
            print("Invalid input: please enter a number between 1 and 5. \n")
            continue

        if choice == 1:
            # Add a new assignment
            name = input("Give this assignment a name: ")
            if tracker.find_assignment(name) is None:
                due_date = input("When is it due? ")
                due_time = input("What time is it due? ")
                tracker.add_assignment(Assignment(name, due_date, due_time))
            else:
                print(f"Invalid name: {name} already exists!")
        elif choice == 2:
            # Delete an assignment
            tracker.print_sorted_assignments()
            to_remove = input("Which assignment would you like to delete? ")
            tracker.remove_assignment(to_remove)
        elif choice == 3:
            # Modify an assignment's name, due date, or due time
            modify = input(" 1. Change Name\n 2. Change Due Date\n 3. Change Due Time ")
            tracker.print_sorted_assignments()
            assignment_name = input("Which assignment do you want to change? ")
            assignment = tracker.find_assignment(assignment_name)
            if assignment:
                try:
                    modify = int(modify)
                    if modify == 1:
                        new_name = input("New assignment name? ")
                        tracker.change_name(assignment, new_name)
                    elif modify == 2:
                        new_date = input("New due date? ")
                        tracker.change_due_date(assignment, new_date)
                    elif modify == 3:
                        new_time = input("New due time? ")
                        tracker.change_due_time(assignment, new_time)
                    else:
                        print("Invalid input: please enter 1, 2, or 3. \n")
                except ValueError:
                    print("Invalid input: please enter a number between 1 and 5. \n")
        elif choice == 4:
            # Print all assignments sorted by due date
            tracker.print_sorted_assignments()
        elif choice == 5:
            # Prints assignments that are due within the upcoming week
            tracker.print_weeks_assignments()
        elif choice == 6:
            # Exit the program
            tracker.conn.close()
            break


if __name__ == "__main__":
    main()
