from CourseAsCode.Models.Custom_Assignment import Custom_Assignment
from CourseAsCode.Services.Custom_Activity_Service import Custom_Activity_Service
from CourseAsCode.Services.Generic_files_Service import Generic_files_Service
from CourseAsCode.Utils.Config_utils import get_tag_config, get_tag_config_boolean, get_tag_config_date
from CourseAsCode.Utils.yaml_parser import get_yaml
import xml.etree.ElementTree as ET
from CourseAsCode.Utils import Tag_Creator

import time


# This file is intended to show how adding a new activity should go

class Assign_Service(Custom_Activity_Service):
    @staticmethod
    def create_activity(assignment_path, id, section_id, config):
        assign_config = get_yaml(assignment_path)
        assignment = Custom_Assignment(id,
                                       section_id,
                                       "assign",
                                       assign_config["name"],
                                       "activities/assign_" + str(id),
                                       assign_config["activity"],
                                       assign_config,
                                       config)
        return assignment

    def assign_gen_files(self, act_directory):
        gfs = Generic_files_Service()
        gfs.create_roles_xml(act_directory)
        gfs.create_calendar_xml(act_directory)
        gfs.create_grade_hist_xml(act_directory)
        gfs.create_filters_xml(act_directory)

    def inforef_xml(self, act_directory, assign: Custom_Assignment):
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

    def assign_xml(self, act_directory, assignment: Custom_Assignment):
        tc = Tag_Creator
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
        tc.create_tag(assign, "alwaysshowdescription", get_tag_config_boolean(assignment.config, "alwaysshowdescription", str(1)), [])
        tc.create_tag(assign, "submissiondrafts", str(0), [])
        tc.create_tag(assign, "sendnotifications", get_tag_config_boolean(assignment.config, "sendnotifications", str(0)), [])
        tc.create_tag(assign, "sendlatenotifications", get_tag_config_boolean(assignment.config, "sendlatenotifications", str(1)), [])
        tc.create_tag(assign, "sendstudentnotifications", get_tag_config_boolean(assignment.config, "sendstudentnotifications", str(1)), [])
        tc.create_tag(assign, "duedate", get_tag_config_date(assignment.assign_config, "finishdate", str(0)), [])
        tc.create_tag(assign, "cutoffdate", get_tag_config_date(assignment.assign_config, "cutoffdate", str(0)), [])
        tc.create_tag(assign, "gradingduedate", get_tag_config_date(assignment.assign_config, "gradingduedate", str(0)), [])
        tc.create_tag(assign, "allowsubmissionsfromdate", get_tag_config_date(assignment.assign_config, "startdate", str(0)), [])
        tc.create_tag(assign, "grade", get_tag_config(assignment.assign_config, "grade", str(10.00000)), [])
        tc.create_tag(assign, "timemodified", str(round(time.time())), [])
        tc.create_tag(assign, "completionsubmit", get_tag_config_boolean(assignment.config, "requiresubmit", str(0)), [])
        tc.create_tag(assign, "requiresubmissionstatement", get_tag_config_boolean(assignment.config, "requiresubmissionstatement", str(1)), [])
        tc.create_tag(assign, "teamsubmission", get_tag_config_boolean(assignment.config, "teamsubmission", str(0)), [])
        tc.create_tag(assign, "requireallteammemberssubmit", get_tag_config_boolean(assignment.config, "requireallteammembers", str(0)), [])
        tc.create_tag(assign, "teamsubmissiongroupingid", str(0), [])
        tc.create_tag(assign, "blindmarking", str(0), [])
        tc.create_tag(assign, "hidegrader", str(0), [])
        tc.create_tag(assign, "revealidentities", str(0), [])
        tc.create_tag(assign, "attemptreopenmethod", get_tag_config(assignment.config, "additionalattempts", str("manual")), [])  # todo: add?
        tc.create_tag(assign, "maxattempts", get_tag_config(assignment.config, "maxattempts", str(-1)), [])
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
                        tc.create_tag(plugin, "value", get_tag_config_boolean(assignment.config, "onlinetext", str(0)), [])
                    case "wordlimit":
                        plugin = ET.SubElement(plugins, "plugin_config")
                        plugin.set("id", str(assignment.module_id + plugin_id))
                        plugin_id += 1
                        tc.create_tag(plugin, "plugin", "onlinetext", [])
                        tc.create_tag(plugin, "subtype", "assignsubmission", [])
                        tc.create_tag(plugin, "name", "wordlimit", [])
                        tc.create_tag(plugin, "value", get_tag_config(assignment.config, "wordlimit", ""), [])
                        plugin = ET.SubElement(plugins, "plugin_config")
                        plugin.set("id", str(assignment.module_id + plugin_id))
                        tc.create_tag(plugin, "plugin", "onlinetext", [])
                        tc.create_tag(plugin, "subtype", "assignsubmission", [])
                        tc.create_tag(plugin, "name", "wordlimitenabled", [])
                        tc.create_tag(plugin, "value", "1", [])
                    case "filesubmissions":
                        plugin = ET.SubElement(plugins, "plugin_config")
                        plugin.set("id", str(assignment.module_id + plugin_id))
                        tc.create_tag(plugin, "plugin", "file", [])
                        tc.create_tag(plugin, "subtype", "assignsubmission", [])
                        tc.create_tag(plugin, "name", "enabled", [])
                        tc.create_tag(plugin, "value", get_tag_config_boolean(assignment.config, "filesubmissions", str(0)), [])
                    case "fileuploads":
                        plugin = ET.SubElement(plugins, "plugin_config")
                        plugin.set("id", str(assignment.module_id + plugin_id))
                        tc.create_tag(plugin, "plugin", "file", [])
                        tc.create_tag(plugin, "subtype", "assignsubmission", [])
                        tc.create_tag(plugin, "name", "maxfilesubmissions", [])
                        tc.create_tag(plugin, "value", get_tag_config(assignment.config, "fileuploads", str(1)), [])
                    case "filetypes":
                        plugin = ET.SubElement(plugins, "plugin_config")
                        plugin.set("id", str(assignment.module_id + plugin_id))
                        tc.create_tag(plugin, "plugin", "file", [])
                        tc.create_tag(plugin, "subtype", "assignsubmission", [])
                        tc.create_tag(plugin, "name", "enabled", [])
                        tc.create_tag(plugin, "value", get_tag_config(assignment.config, "filetypes", "any"), [])

                plugin_id += 1

        tc.create_tag(assign, "overrides", "", [])
        tree = ET.ElementTree(activity)
        tree.write(act_directory + "/assign.xml", encoding='utf-8', xml_declaration=True)

    def grades_xml(self, act_directory, act: Custom_Assignment):
        activity_gradebook = ET.Element("activity_gradebook")
        grade_items = ET.SubElement(activity_gradebook, "grade_items")

        grade_item = ET.SubElement(grade_items, "grade_item")
        grade_item.set("id", str(act.module_id))
        grade_item.tail = '\n'

        categoryid = ET.SubElement(grade_item, "categoryid")
        categoryid.text = str(act.module_id)  # 41545 todo:
        categoryid.tail = '\n'

        itemname = ET.SubElement(grade_item, "itemname")
        itemname.text = act.name
        itemname.tail = '\n'

        itemtype = ET.SubElement(grade_item, "itemtype")
        itemtype.text = "mod"
        itemtype.tail = '\n'

        itemmodule = ET.SubElement(grade_item, "itemmodule")
        itemmodule.text = "quiz"
        itemmodule.tail = '\n'

        iteminstance = ET.SubElement(grade_item, "iteminstance")
        iteminstance.text = str(60671)  # 2 todo: id
        iteminstance.tail = '\n'

        itemnumber = ET.SubElement(grade_item, "itemnumber")
        itemnumber.text = str(0)
        itemnumber.tail = '\n'

        iteminfo = ET.SubElement(grade_item, "iteminfo")
        iteminfo.text = "$@NULL@$"
        iteminfo.tail = '\n'

        idnumber = ET.SubElement(grade_item, "idnumber")
        idnumber.tail = '\n'

        calculation = ET.SubElement(grade_item, "calculation")
        calculation.text = "$@NULL@$"
        calculation.tail = '\n'

        gradetype = ET.SubElement(grade_item, "gradetype")
        gradetype.text = str(1)
        gradetype.tail = '\n'

        grademax = ET.SubElement(grade_item, "grademax")
        grademax.text = str(10.00000)
        grademax.tail = '\n'

        grademin = ET.SubElement(grade_item, "grademin")
        grademin.text = str(0.00000)
        grademin.tail = '\n'

        scaleid = ET.SubElement(grade_item, "scaleid")
        scaleid.text = "$@NULL@$"
        scaleid.tail = '\n'

        outcomeid = ET.SubElement(grade_item, "outcomeid")
        outcomeid.text = "$@NULL@$"
        outcomeid.tail = '\n'

        gradepass = ET.SubElement(grade_item, "gradepass")
        gradepass.text = str(0.00000)
        gradepass.tail = '\n'

        multfactor = ET.SubElement(grade_item, "multfactor")
        multfactor.text = str(1.00000)
        multfactor.tail = '\n'

        plusfactor = ET.SubElement(grade_item, "plusfactor")
        plusfactor.text = str(0.00000)
        plusfactor.tail = '\n'

        aggregationcoef = ET.SubElement(grade_item, "aggregationcoef")
        aggregationcoef.text = str(0.00000)
        aggregationcoef.tail = '\n'

        aggregationcoef2 = ET.SubElement(grade_item, "aggregationcoef2")
        aggregationcoef2.text = str(1.00000)
        aggregationcoef2.tail = '\n'

        weightoverride = ET.SubElement(grade_item, "weightoverride")
        weightoverride.text = str(0)
        weightoverride.tail = '\n'

        sortorder = ET.SubElement(grade_item, "sortorder")
        sortorder.text = str(2)
        sortorder.tail = '\n'

        display = ET.SubElement(grade_item, "display")
        display.text = str(0)
        display.tail = '\n'

        decimals = ET.SubElement(grade_item, "decimals")
        decimals.text = "$@NULL@$"
        decimals.tail = '\n'

        hidden = ET.SubElement(grade_item, "hidden")
        hidden.text = str(1)
        hidden.tail = '\n'

        locked = ET.SubElement(grade_item, "locked")
        locked.text = str(0)
        locked.tail = '\n'

        locktime = ET.SubElement(grade_item, "locktime")
        locktime.text = str(0)
        locktime.tail = '\n'

        needsupdate = ET.SubElement(grade_item, "needsupdate")
        needsupdate.text = str(0)
        needsupdate.tail = '\n'

        timecreated = ET.SubElement(grade_item, "timecreated")
        timecreated.text = str(1688645726)
        timecreated.tail = '\n'

        timemodified = ET.SubElement(grade_item, "timemodified")
        timemodified.text = str(1688723921)
        timemodified.tail = '\n'

        grade_grades = ET.SubElement(grade_item, "grade_grades")
        grade_grades.tail = '\n'

        grade_letters = ET.SubElement(activity_gradebook, "grade_letters")
        grade_letters.tail = '\n'

        tree = ET.ElementTree(activity_gradebook)
        tree.write(act_directory + "/grades.xml", encoding='utf-8', xml_declaration=True)

    @staticmethod
    def generate_xmls(act_directory, act):
        c = Assign_Service()
        c.assign_gen_files(act_directory)
        c.inforef_xml(act_directory, act)
        c.assign_xml(act_directory, act)
        c.grades_xml(act_directory, act)
