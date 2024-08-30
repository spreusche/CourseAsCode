from CourseAsCode.Models.Activity import Activity


class Assignment(Activity):
    def __init__(self, moduleid, sectionid, modulename, title, directory, text, config):
        super().__init__(moduleid, sectionid, modulename, title, directory, text)
        self.link = "$@ASSIGNVIEWBYID*" + str(self.module_id) + "@$"
        # geteo las cosas de la config
        self.config = config
        self.name = title


        