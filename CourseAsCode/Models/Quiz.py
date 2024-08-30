from CourseAsCode.Models.Activity import Activity


class Quiz(Activity):
    def __init__(self, moduleid, name, section_id, modulename, directory, text, config):
        super().__init__(moduleid, section_id, modulename, name, directory, text, config)
        self.id = moduleid
        self.name = name
        self.intro = None
        self.questions = []
        self.last_question_id = 0

