class Course:
    def __init__(self, id, contextid, sections, config):
        self.id = id
        self.context_id = contextid
        self.http_origin = "https://moodle.technikum-wien.at"  # Todo: default for FH TK
        self.sections = sections
        self.config = config

        course_defaults = {
            "courseName": "courseName",
            "category": "miscellaneous",
            "summary": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
            "visibility": "Show",
            "startDate": "31-08-2023 23:59h",
            "endDate": "31-08-2024 23:59h",
            "IDnumber": "",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            "format": "scfhtw",
            "assessment": "",
            "assessmentCriteria": "",
            "showHeader": True,
            "showCourseImage": False,
            "showTeachers": True,
            "numTeachersInBox": "2",  #
            "teacherBoxTitle": "Lecturers",  #
            "showOverview": True,  #
            "showInfobox": True,  #

            # - APPEARANCE - #
            "language": "en",
            "numAnnouncements": "5",  # 0-10
            "showGradebook": True,  #
            "showActivityReports": True,  #
            "showActivityDates": True,  #

            # - FILES AND UPLOADS - #
            "maxUploadSize": "500 MB",  # 10 KB - 2 GB
            "legacyFiles": True,  # default yes

            # - COMPLETION TRACKING - #
            "enableCompletionTracking": False,  #

            # - GROUPS - #
            "groupMode": "2",  # 0: no groups - 1: separate groups - 2: visible groups
            "forceGroupMode": False,
            "defaultGrouping": False
        }

        for key in course_defaults:
            if key not in config:
                self.config[key] = course_defaults[key]

        self.name = config["courseName"]
        self.shortname = config["courseName"]
        self.course_format = config["format"]  # "scfhtw" #Todo: default for FH TK
        self.lang = config["language"]  # "en" #default will be english




    def set_format(self, formt):
        self.course_format = formt

    def set_http_origin(self, origin):
        self.http_origin = origin

    def set_lang(self, lang):
        self.lang = lang
