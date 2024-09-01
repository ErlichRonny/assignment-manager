# Assignment Manager

# Features:
Create Assignments: Add new assignments with a name, due date, and time.

Edit Assignments: Update assignment details, including name, due date, and time.

Track Assignments: View assignments due within the week or on specific dates.

Responsive UI: Clean and responsive user interface built using Bootstrap.

SQLite Database: Efficient database for storing assignment data.
  
# File Descriptions:
- 'app.py': Main Flask application file, implements web app routes.
- 'assignment_manager.py': Manages assignments (creating, updating, retrieving data) and interacts with SQLite database
- 'assignment.py': Defines Assignment class, where assignments have a name, due date, due time, and completion status. Provides methods to change and retrieve assignment data.
- 'cli.py': Old command-line interface for managing assignments.
- 'test-assignment-manager.py': Contains unit tests for AssignmentManager class.
- 'templates/base.html': Base template for the application that other templates extend.
- 'templates/view_assignments.html': Template used to display/manage assignments, has functionality for viewing, editing, adding, and deleting assignments through a user interface.
