from CourseAsCode.Models.Activity import Activity

# This file is intended to show how adding a new activity should go


class Custom_Assignment(Activity):
    def __init__(self, moduleid, sectionid, modulename, title, directory, text, assign_config, config):
        super().__init__(moduleid, sectionid, modulename, title, directory, text, config)
        self.link = "$@ASSIGNVIEWBYID*" + str(self.module_id) + "@$"
        self.assign_config = assign_config
        self.name = title

        # note that config stands for the general config that every activity can have.
        # In this case will have everything other than name, dates and score
