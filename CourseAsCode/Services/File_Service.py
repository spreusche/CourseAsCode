import time

from CourseAsCode.Services.Activity_Service import Activity_Service
import xml.etree.ElementTree as ET

from CourseAsCode.Utils.Config_utils import get_tag_config


class File_Service:
    @staticmethod
    def generate_activity_gen_files(act_directory):
        Activity_Service.calendar_xml(act_directory)
        Activity_Service.roles_xml(act_directory)
        Activity_Service.grades_xml(act_directory)
        Activity_Service.grade_history_xml(act_directory)
        Activity_Service.filters_xml(act_directory)

    @staticmethod
    def inforef_xml(file, resource_directory):
        inforef = ET.Element("inforef")
        fileref = ET.SubElement(inforef, "fileref")

        filet = ET.SubElement(fileref, "file")
        fileid = ET.SubElement(filet, "id")
        fileid.text = str(file.module_id)
        fileid.tail = '\n'
        tree = ET.ElementTree(inforef)
        tree.write(resource_directory + "/inforef.xml", encoding="utf-8", xml_declaration=True)

    @staticmethod
    def resource_xml(resource_directory, file):
        activity = ET.Element("activity")
        activity.set("id", str(file.module_id))
        activity.set("moduleid", str(file.module_id))
        activity.set("modulename", "resource")
        activity.set("contextid", str(file.module_id))

        res = ET.SubElement(activity, "resource")
        res.set("id", str(file.module_id))

        name = ET.SubElement(res, "name")
        name.text = file.name
        name.tail = '\n'

        intro = ET.SubElement(res, "intro")
        intro.text = get_tag_config(file.config, "intro", "")
        intro.tail = '\n'

        introformat = ET.SubElement(res, "introformat")
        introformat.text = str(1)
        introformat.tail = '\n'

        tobemigrated = ET.SubElement(res, "tobemigrated")
        tobemigrated.text = str(0)
        tobemigrated.tail = '\n'

        legacyfiles = ET.SubElement(res, "legacyfiles")
        legacyfiles.text = str(0)
        legacyfiles.tail = '\n'

        legacyfileslast = ET.SubElement(res, "legacyfileslast")
        legacyfileslast.text = "$@NULL@$"
        legacyfileslast.tail = '\n'

        display = ET.SubElement(res, "display")
        display.text = get_display(file.config, "display", str(0))
        display.tail = '\n'

        displayoptions = ET.SubElement(res, "displayoptions")
        displayoptions.text = "a:1:{s:10:\"printintro\";i:1;}"
        displayoptions.tail = '\n'

        filterfiles = ET.SubElement(res, "filterfiles")
        filterfiles.text = str(0)
        filterfiles.tail = '\n'

        revision = ET.SubElement(res, "revision")
        revision.text = str(0)
        revision.tail = '\n'

        timemodified = ET.SubElement(res, "timemodified")
        timemodified.text = str(time.time())
        timemodified.tail = '\n'

        tree = ET.ElementTree(activity)
        tree.write(resource_directory + "/resource.xml", encoding="utf-8", xml_declaration=True)


def get_display(config, wanted_config: str, default: str):
    if config is not None and wanted_config in config:
        match config[wanted_config].lower():
            case "automatic":
                return str(0)
            case "embed":
                return str(1)
            case "download":
                return str(2)
            case "open":
                return str(3)
            case "popup":
                return str(4)

    return default



