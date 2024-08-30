from CourseAsCode.Models.Question import Question


class Question_multichoice(Question):
    def __init__(self, id, qtype, title, text, feedback):
        super().__init__(id, "multichoice", title, text, feedback)
        self.correct = []
        self.incorrect = []