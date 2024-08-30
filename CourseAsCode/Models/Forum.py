import time

from CourseAsCode.Models.Activity import Activity


class Forum(Activity):
    def __init__(self, moduleid, sectionid, modulename, title, directory, text, config):
        super().__init__(moduleid, sectionid, modulename, title, directory, text, config)
        self.link = "$@FORUMVIEWBYID*" + str(self.module_id) + "@$"
        #Default forum:
        self.type = "general"
        self.introformat = "1"
        self.duedate = "0"
        self.cutoffdate = "0"
        self.assessed = "0"
        self.assesstimestart = "0"
        self.assesstimefinish = "0"
        self.scale = "100"
        self.maxbytes = "512000" # 5 KB
        self.maxattachments = "9"
        self.forcesubscribe = "0"
        self.trackingtype = "1"
        self.rsstype = "0"
        self.rssarticles = "0"
        self.timemodified = str(int(time.time()))
        self.warnafter = "0"
        self.blockafter = "0"
        self.blockperiod = "0"
        self.completiondiscussions = "0"
        self.completionreplies = "0"
        self.completionposts = "0"
        self.displaywordcount = "0"
        self.lockdiscussionafter = "0"
        self.grade_forum = "0"
