from CourseAsCode.Models.Activity import Activity


class Label(Activity):
    def __init__(self, moduleid, sectionid, modulename, title, directory, text, config):
        super().__init__(moduleid, sectionid, modulename, title, directory, text, config)
        self.link = "$@LABELVIEWBYID*" + str(self.module_id) + "@$"

