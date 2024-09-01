from datetime import datetime
import dateparser

class Assignment:
    """
    Represents assignments with a name, due date, and due time.
    """

    def __init__(self, name: str, due_date: str, due_time: str, done: bool):
        """
        Initializes assignments with name, due date, due time
        """
        self.name = name
        self.due_date = datetime.strptime(due_date, "%Y-%m-%d")
        self.due_time = datetime.strptime(due_time, "%H:%M")
        self.done = done

    def get_due_str(self) -> str:
        """
        Gets formatted due date/time as a string
        """
        return f"due on {self.due_date.strftime('%a, %m/%d/%y')} at {self.due_time.strftime('%I:%M %p')}"

    def set_name(self, new_name: str) -> None:
        """
        Sets a new name for the assigment
        """
        self.name = new_name

    def set_due_date(self, new_due_date: str) -> None:
        """
        Sets a new due date for the assignment
        """
        self.due_date = dateparser.parse(new_due_date).date()

    def set_due_time(self, new_due_time: str) -> None:
        """
        Sets a new due time for the assignment
        """
        self.due_time = dateparser.parse(new_due_time).time()

    def set_done(self, done: bool) -> None:
        """
        Sets completion status of an assignment
        """
        self.done = done

    def to_dictionary(self) -> dict:
        """
        Convers assignment to a dictionary for serializatoin
        """
        # datetime objects are not directly serializable, need to convert to string
        return {
            "name": self.name,
            "due_date": self.due_date.strftime("%Y-%m-%d"),
            "due_time": self.due_time.strftime("%H:%M"),
        }
