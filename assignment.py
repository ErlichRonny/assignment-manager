from datetime import datetime
import dateparser

class Assignment:
    """
    Represents assignments with a name, due date, and due time.
    """

    def __init__(self, name, due_date, due_time):
        """
        Initializes assignments with name, due date, due time
        """
        self.name = name
        self.due_date = datetime.strptime(due_date, "%Y-%m-%d")
        self.due_time = datetime.strptime(due_time, "%H:%M")

    def get_due(self):
        """
        Gets combined datetime object with due date and due time
        """
        return datetime.combine(self.due_date, self.due_time)

    def get_due_str(self):
        """
        Gets formatted due date/time as a string
        """
        return f"due on {self.due_date.strftime('%a, %m/%d/%y')} at {self.due_time.strftime('%I:%M %p')}"

    def set_name(self, new_name):
        """
        Sets a new name for the assigment
        """
        self.name = new_name

    def set_due_date(self, new_due_date):
        """
        Sets a new due date for the assignment
        """
        self.due_date = dateparser.parse(new_due_date).date()

    def set_due_time(self, new_due_time):
        """
        Sets a new due time for the assignment
        """
        self.due_time = dateparser.parse(new_due_time).time()

    def to_dictionary(self):
        # datetime objects are not directly serializable, need to convert to string
        new_dict = {
            "name": self.name,
            "due_date": self.due_date.strftime("%Y-%m-%d"),
            "due_time": self.due_time.strftime("%H:%M"),
        }
        return new_dict
