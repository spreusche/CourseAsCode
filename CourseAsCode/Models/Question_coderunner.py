from CourseAsCode.Models.Question import Question


class Question_coderunner(Question):
    def __init__(self, id, qtype, title, text, feedback):
        super().__init__(id, "coderunner", title, text, feedback)
        self.coderunner_type = None
        self.answer_preload = None
        self.answer = None
        self.tests = [] # Test array




