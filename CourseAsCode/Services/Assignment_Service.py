import time

from CourseAsCode.Models.Assignment import Assignment
import xml.etree.ElementTree as ET

from CourseAsCode.Services.Generic_files_Service import Generic_files_Service
from CourseAsCode.Utils import Tag_Creator
from CourseAsCode.Utils.yaml_parser import get_yaml


# assign, grades, grading, inforef,
class Assignment_Service:
    @staticmethod
    def parse_assign(assignment_path, id, section_id):
        assign_config = get_yaml(assignment_path)
        assignment = Assignment(id,
                                section_id,
                                "assign",
                                assign_config["name"],
                                "activities/assign_" + str(id),
                                assign_config["activity"],
                                assign_config)
        return assignment

    @staticmethod
    def assign_gen_files(act_directory):
        gfs = Generic_files_Service()
        gfs.create_roles_xml(act_directory)
        gfs.create_calendar_xml(act_directory)
        gfs.create_grade_hist_xml(act_directory)
        gfs.create_filters_xml(act_directory)

    @staticmethod
    def inforef_xml(act_directory, assign: Assignment):
        inforef = ET.Element("inforef")
        grade_itemref = ET.SubElement(inforef, "grade_itemref")
        grade_itemref.tail = '\n'
        grade_item = ET.SubElement(grade_itemref, "grade_item")
        grade_item.tail = '\n'
        id = ET.SubElement(grade_item, "id")
        id.text = str(assign.module_id)  # todo: should be a real grade item id
        id.tail = '\n'

        tree = ET.ElementTree(inforef)
        tree.write(act_directory + "/inforef.xml", encoding='utf-8', xml_declaration=True)
    @staticmethod
    def assign_xml(act_directory, assignment: Assignment):
        tc = Tag_Creator
        dateFormat = '%d-%m-%Y %H:%M'
        activity = ET.Element("activity")
        activity.set("id", str(assignment.module_id))
        activity.set("moduleid", str(assignment.module_id))
        activity.set("modulename", "assignment")
        activity.set("contextid", str(12345))

        assign = ET.SubElement(activity, "assign")
        assign.set("id", str(assignment.module_id))

        tc.create_tag(assign, "name", str(assignment.title), [])
        tc.create_tag(assign, "intro", str(assignment.intro), [])
        tc.create_tag(assign, "introformat", str(1), [])
        tc.create_tag(assign, "alwaysshowdescription", str(1), [])
        tc.create_tag(assign, "submissiondrafts", str(0), [])
        tc.create_tag(assign, "sendnotifications", str(0), [])
        tc.create_tag(assign, "sendlatenotifications", str(1), [])
        tc.create_tag(assign, "sendstudentnotifications", str(1), [])
        parsed_time = time.strptime(assignment.config["finishdate"], dateFormat)
        timestamp = time.mktime(parsed_time)
        tc.create_tag(assign, "duedate", str(int(timestamp)), [])
        tc.create_tag(assign, "cutoffdate", str(0), [])
        tc.create_tag(assign, "gradingduedate", str(0), [])
        parsed_time = time.strptime(assignment.config["startdate"], dateFormat)
        timestamp = time.mktime(parsed_time)
        tc.create_tag(assign, "allowsubmissionsfromdate", str(int(timestamp)), [])
        tc.create_tag(assign, "grade", str(assignment.config["grade"]), [])
        tc.create_tag(assign, "timemodified", str(round(time.time())), [])
        tc.create_tag(assign, "completionsubmit", str(0), [])
        tc.create_tag(assign, "requiresubmissionstatement", str(1), [])
        tc.create_tag(assign, "teamsubmission", str(0), [])
        tc.create_tag(assign, "requireallteammemberssubmit", str(0), [])
        tc.create_tag(assign, "teamsubmissiongroupingid", str(0), [])
        tc.create_tag(assign, "blindmarking", str(0), [])
        tc.create_tag(assign, "hidegrader", str(0), [])
        tc.create_tag(assign, "revealidentities", str(0), [])
        tc.create_tag(assign, "attemptreopenmethod", str("manual"), [])  # todo: add?
        tc.create_tag(assign, "maxattempts", str(-1), [])  # todo: add?
        tc.create_tag(assign, "markingworkflow", str(0), [])
        tc.create_tag(assign, "markingallocation", str(0), [])
        tc.create_tag(assign, "preventsubmissionnotingroup", str(0), [])
        tc.create_tag(assign, "userflags", "", [])
        tc.create_tag(assign, "submissions", "", [])
        tc.create_tag(assign, "grades", "", [])

        plugins = ET.SubElement(assign, "plugin_configs")

        additional_settings = ["onlinetext", "filesubmissions", "fileuploads",
                               "wordlimit", "filetypes"]

        plugin_id = 1
        for setting in assignment.config:
            if setting in additional_settings:
                match setting:
                    case "onlinetext":
                        plugin = ET.SubElement(plugins, "plugin_config")
                        plugin.set("id", str(assignment.module_id + plugin_id))
                        tc.create_tag(plugin, "plugin", setting, [])
                        tc.create_tag(plugin, "subtype", "assignsubmission", [])
                        tc.create_tag(plugin, "name", "enabled", [])
                        tc.create_tag(plugin, "value", "1" if str(assignment.config[setting]) else "0", [])
                    case "wordlimit":
                        plugin = ET.SubElement(plugins, "plugin_config")
                        plugin.set("id", str(assignment.module_id + plugin_id))
                        plugin_id += 1
                        tc.create_tag(plugin, "plugin", setting, [])
                        tc.create_tag(plugin, "subtype", "assignsubmission", [])
                        tc.create_tag(plugin, "name", "wordlimit", [])
                        tc.create_tag(plugin, "value", str(assignment.config[setting]), [])
                        plugin = ET.SubElement(plugins, "plugin_config")
                        plugin.set("id", str(assignment.module_id + plugin_id))
                        tc.create_tag(plugin, "plugin", setting, [])
                        tc.create_tag(plugin, "subtype", "assignsubmission", [])
                        tc.create_tag(plugin, "name", "wordlimitenabled", [])
                        tc.create_tag(plugin, "value", "1", [])
                    case "filesubmissions":
                        plugin = ET.SubElement(plugins, "plugin_config")
                        plugin.set("id", str(assignment.module_id + plugin_id))
                        tc.create_tag(plugin, "plugin", "file", [])
                        tc.create_tag(plugin, "subtype", "assignsubmission", [])
                        tc.create_tag(plugin, "name", "enabled", [])
                        tc.create_tag(plugin, "value", "1" if str(assignment.config[setting]) else "0", [])
                    case "fileuploads":
                        plugin = ET.SubElement(plugins, "plugin_config")
                        plugin.set("id", str(assignment.module_id + plugin_id))
                        tc.create_tag(plugin, "plugin", "file", [])
                        tc.create_tag(plugin, "subtype", "assignsubmission", [])
                        tc.create_tag(plugin, "name", "maxfilesubmissions", [])
                        tc.create_tag(plugin, "value", str(assignment.config[setting]), [])
                    case "filetypes":
                        plugin = ET.SubElement(plugins, "plugin_config")
                        plugin.set("id", str(assignment.module_id + plugin_id))
                        tc.create_tag(plugin, "plugin", "file", [])
                        tc.create_tag(plugin, "subtype", "assignsubmission", [])
                        tc.create_tag(plugin, "name", "enabled", [])
                        tc.create_tag(plugin, "value", str(assignment.config[setting]), [])

                plugin_id += 1

        tc.create_tag(assign, "overrides", "", [])
        tree = ET.ElementTree(activity)
        tree.write(act_directory + "/assign.xml", encoding='utf-8', xml_declaration=True)

