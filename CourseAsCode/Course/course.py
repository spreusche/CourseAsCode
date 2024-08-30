import sys
import xml.etree.ElementTree as ET
from CourseAsCode.Utils import Tag_Creator
from CourseAsCode.Models import Course
import time
from datetime import datetime

from CourseAsCode.Utils.getBytes import getBytes


# id: it is used at: questions.xml -> <contextinstanceid>
#                   moodle_backup.xml -> <original_course_id> and <courseid>
# contextid: it is used at: files.xml, questions.xml, moodle_backup.xml, block.xml as contextid or originalcontextid


def create_xml(course_dir, c: Course):
    course = ET.Element("course")
    # course.text = '\n'
    course.set("id", str(c.id))
    course.set("contextid", str(c.context_id))

    date_format = "%d-%m-%Y %H:%M"

    # mostly generic tags
    Tag_Creator.create_tag(course, "shortname", c.config["courseName"], [])
    Tag_Creator.create_tag(course, "fullname", c.name, [])
    Tag_Creator.create_tag(course, "idnumber", "", [])
    Tag_Creator.create_tag(course, "summary", c.config["summary"], [])
    Tag_Creator.create_tag(course, "summaryformat", "1", [])
    Tag_Creator.create_tag(course, "format", c.config["format"], [])
    Tag_Creator.create_tag(course, "showgrades", "1" if c.config["showGradebook"] else "0", [])
    Tag_Creator.create_tag(course, "newsitems", str(c.config["numAnnouncements"]), [])
    try:
        Tag_Creator.create_tag(course, "startdate",
                               str(int((datetime.strptime(c.config["startDate"], date_format)).timestamp())),
                               [])
        Tag_Creator.create_tag(course, "enddate",
                               str(int((datetime.strptime(c.config["endDate"], date_format)).timestamp())), [])
    except:
        print("Course config dates must follow the dd-mm-YYY hh:mm format")
        sys.exit(1)
    Tag_Creator.create_tag(course, "marker", "-1", [])
    maxBytes = getBytes(str(c.config["maxUploadSize"]))  # todo
    Tag_Creator.create_tag(course, "maxbytes", str(maxBytes), [])
    Tag_Creator.create_tag(course, "legacyfiles", "1" if c.config["legacyFiles"] else "0", [])
    Tag_Creator.create_tag(course, "showreports", "1" if c.config["showActivityReports"] else "0", [])
    Tag_Creator.create_tag(course, "visible", "1" if c.config["visibility"].lower() == "show" else "0", [])
    Tag_Creator.create_tag(course, "groupmode", str(c.config["groupMode"]), [])
    Tag_Creator.create_tag(course, "groupmodeforce", "1" if c.config["forceGroupMode"] else "0", [])
    Tag_Creator.create_tag(course, "defaultgroupingid", "1" if c.config["defaultGrouping"] else "0", [])
    Tag_Creator.create_tag(course, "lang", c.lang, [])
    Tag_Creator.create_tag(course, "theme", "", [])
    Tag_Creator.create_tag(course, "timecreated", str(int(time.time())), [])
    Tag_Creator.create_tag(course, "timemodified", str(int(time.time())), [])
    Tag_Creator.create_tag(course, "requested", "0", [])
    Tag_Creator.create_tag(course, "showactivitydates", "1" if c.config["showActivityDates"] else "0", [])
    Tag_Creator.create_tag(course, "showcompletionconditions", "0", [])
    Tag_Creator.create_tag(course, "enablecompletion", "1" if c.config["enableCompletionTracking"] else "0", [])
    Tag_Creator.create_tag(course, "completionnotify", "0", [])

    category = ET.SubElement(course, "category")
    category.set("id", "1")
    # category.text = '\n\t'
    category.tail = '\n'
    Tag_Creator.create_tag(category, "name", c.name, [])
    Tag_Creator.create_tag(category, "description", "", [])

    Tag_Creator.create_tag(course, "tags", "", [])
    courseformatoptions = ET.SubElement(course, "courseformatoptions")

    options = ["blockname", "sectionblock", "sectionstartdate", "sectiontype"]
    for section in c.sections:
        for option in options:
            courseformatoption = ET.SubElement(courseformatoptions, "courseformatoption")
            Tag_Creator.create_tag(courseformatoption, "format", c.course_format, [])
            Tag_Creator.create_tag(courseformatoption, "sectionid", str(section.id), [])
            Tag_Creator.create_tag(courseformatoption, "name", option, [])
            match option:
                case "blockname":
                    Tag_Creator.create_tag(courseformatoption, "value", "", [])
                case "sectionblock":
                    Tag_Creator.create_tag(courseformatoption, "value", "0", [])
                case "sectionstartdate":
                    Tag_Creator.create_tag(courseformatoption, "value", "$@NULL@$", [])
                case "sectiontype":
                    Tag_Creator.create_tag(courseformatoption, "value", "0", [])

    tree = ET.ElementTree(course)
    tree.write(course_dir + "/course.xml", encoding='utf-8', xml_declaration=True)