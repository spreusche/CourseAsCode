import xml.etree.ElementTree as ET

from CourseAsCode.Models import Course
from CourseAsCode.Utils import Tag_Creator
import time

from CourseAsCode.Models.File import File


def change_first_line(xml_path):
    with open(xml_path) as f:
        lines = f.readlines()
    lines[0] = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    with open(xml_path, "w") as f:
        f.writelines(lines)


def create_xml(backup_dir, filename, c: Course):
    # Create a new XML tree
    moodle_backup = ET.Element("moodle_backup")
    #moodle_backup.text = '\n\t'

    information = ET.SubElement(moodle_backup, "information")
    #information.text = '\n\t'

    Tag_Creator.create_tag(information, "name", filename, [])
    Tag_Creator.create_tag(information, "moodle_version", "2021051711.08", [])
    Tag_Creator.create_tag(information, "moodle_release", "3.11.11+ (Build: 20230105)", [])
    Tag_Creator.create_tag(information, "backup_version", "2021051700", [])
    Tag_Creator.create_tag(information, "backup_release", "3.11", [])
    Tag_Creator.create_tag(information, "backup_date", str(int(time.time())), [])
    Tag_Creator.create_tag(information, "mnet_remoteusers", "0", [])  #
    Tag_Creator.create_tag(information, "include_files", "1",
                           [])  # todo: The one I made is in 1, maybe if i put it in 0 it wont include any files?
    Tag_Creator.create_tag(information, "include_file_references_to_external_content", "1", [])
    Tag_Creator.create_tag(information, "original_wwwroot", c.http_origin, [])
    Tag_Creator.create_tag(information, "original_site_identifier_hash", "6118578f64415b7ca246939bfb24e84a", [])
    Tag_Creator.create_tag(information, "original_course_id", str(c.id), [])
    Tag_Creator.create_tag(information, "original_course_format", c.course_format, [])
    Tag_Creator.create_tag(information, "original_course_fullname", c.name, [])
    Tag_Creator.create_tag(information, "original_course_shortname", c.shortname, [])
    Tag_Creator.create_tag(information, "original_course_startdate", str(int(time.time())), [])
    Tag_Creator.create_tag(information, "original_course_enddate", "0", [])
    Tag_Creator.create_tag(information, "original_course_contextid", str(c.context_id), [])
    Tag_Creator.create_tag(information, "original_system_contextid", "1", [])

    details = ET.SubElement(information, "details")
   # details.text = '\n\t'
    details.tail = '\n'
    detail = ET.SubElement(details, "detail")
    detail.set("backup_id", "85b0c0f4289ac9bc83a27bb3c167893c")  # Todo: unnecesary?
    #detail.text = '\n\t'
    detail.tail = '\n'

    Tag_Creator.create_tag(detail, "type", "course", [])
    Tag_Creator.create_tag(detail, "format", "moodle2", [])
    Tag_Creator.create_tag(detail, "interactive", "1", [])
    Tag_Creator.create_tag(detail, "mode", "10", [])
    Tag_Creator.create_tag(detail, "execution", "1", [])
    Tag_Creator.create_tag(detail, "executiontime", "0", [])

    contents = ET.SubElement(information, "contents")
    #contents.text = '\n\t'
    contents.tail = '\n'
    activities = ET.SubElement(contents, "activities")
    #activities.text = '\n\t'
    activities.tail = '\n'

    for section in c.sections:
        section_acts_in_order = [item for sublist in section.activities.values() for item in sublist]
        section_acts_in_order = sorted(section_acts_in_order, key=lambda x: int(x.module_id))
        # for module in section.activities:
        for act in section_acts_in_order:
            activity = ET.SubElement(activities, "activity")
            Tag_Creator.create_tag(activity, "moduleid", str(act.module_id), [])
            Tag_Creator.create_tag(activity, "sectionid", str(section.id), [])
            Tag_Creator.create_tag(activity, "modulename", act.module_name, [])
            if isinstance(act, File):
                Tag_Creator.create_tag(activity, "title", act.name, [])
            else:
                Tag_Creator.create_tag(activity, "title", act.title, [])
            Tag_Creator.create_tag(activity, "directory", act.directory, [])

    sections = ET.SubElement(contents, "sections")
    sections.tail = '\n'

    for s in c.sections:
        section = ET.SubElement(sections, "section")
        Tag_Creator.create_tag(section, "sectionid", str(s.id), [])
        Tag_Creator.create_tag(section, "title", s.name, [])
        Tag_Creator.create_tag(section, "directory", s.directory, [])

    course = ET.SubElement(contents, "course")
    course.tail = '\n'
    Tag_Creator.create_tag(course, "courseid", str(c.id), [])
    Tag_Creator.create_tag(course, "title", c.name, [])
    Tag_Creator.create_tag(course, "directory", "course", [])

    settings = ET.SubElement(information, "settings")
    root_settings(settings, filename)

    values = [("userinfo", 0), ("included", 1)]
    for s in c.sections:
        section_settings(settings, s.id, values)
        for module in s.activities:
            for a in s.activities[module]:
                activity_settings(settings, a.module_name, a.module_id, values)
        for file in s.files:
            activity_settings(settings, "resource", file.module_id, values)

    tree = ET.ElementTree(moodle_backup)
    tree.write(backup_dir + "/moodle_backup.xml", encoding="utf-8", xml_declaration=True)
    change_first_line(backup_dir + "/moodle_backup.xml") # patch for <?xml version="1.0" encoding="utf-8"?> instead of <?xml version='1.0' encoding='utf-8'?>



def activity_settings(parent_tag, module_name, id, values):
    for k, v in values:
        setting = ET.SubElement(parent_tag, "setting")
        Tag_Creator.create_tag(setting, "level", "activity", [])
        Tag_Creator.create_tag(setting, "activity", module_name + "_" + str(id), [])
        Tag_Creator.create_tag(setting, "name", module_name + "_" + str(id) + "_" + k, [])
        Tag_Creator.create_tag(setting, "value", str(v), [])


def section_settings(parent_tag, id, values):
    for k, v in values:
        setting = ET.SubElement(parent_tag, "setting")
        Tag_Creator.create_tag(setting, "level", "section", [])
        Tag_Creator.create_tag(setting, "section", "section_" + str(id), [])
        Tag_Creator.create_tag(setting, "name", "section_" + str(id) + "_" + k, [])
        Tag_Creator.create_tag(setting, "value", str(v), [])


def root_settings(parent_tag, filename):
    level = "root"
    # todo: all these are 'yes or no' options done when creting the backup. We could add some configurations in the
    #  future to handle some of these:
    names = [("filename", filename), ("imscc11", 0), ("users", 0), ("anonymize", 0),
             ("role_assignments", 0), ("activities", 1), ("blocks", 1), ("files", 1),
             ("filters", 1), ("comments", 0), ("badges", 0), ("calendarevents", 1), ("userscompletion", 0),
             ("logs", 0), ("grade_histories", 1), ("questionbank", 1), ("groups", 1), ("competencies", 0),
             ("customfield", 1), ("contentbankcontent", 1), ("legacyfiles", 1)
             ]
    for name, value in names:
        setting = ET.SubElement(parent_tag, "setting")
        Tag_Creator.create_tag(setting, "level", level, [])
        Tag_Creator.create_tag(setting, "name", name, [])
        Tag_Creator.create_tag(setting, "value", str(value), [])
