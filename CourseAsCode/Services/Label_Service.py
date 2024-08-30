import xml.etree.ElementTree as ET

from CourseAsCode.Models.Activity import Activity
from CourseAsCode.Utils import Tag_Creator


class Label_Service:
    @staticmethod
    def create_label_xml(act_directory, activity: Activity):
        activity_tag = ET.Element("activity")
        activity_tag.set('id',
                         str(activity.module_id))
        activity_tag.set('moduleid', str(activity.module_id))
        activity_tag.set('modulename', activity.module_name)
        activity_tag.set('contextid',
                         '12345')

        label = ET.SubElement(activity_tag, "label")
        label.set("id", str(activity.module_id))

        Tag_Creator.create_tag(label, "name", activity.title, [])
        Tag_Creator.create_tag(label, "intro", activity.intro, [])
        Tag_Creator.create_tag(label, "introformat", "1", [])
        Tag_Creator.create_tag(label, "timemodified", "1658479891", [])

        tree = ET.ElementTree(activity_tag)
        tree.write(act_directory + "/label.xml", encoding='utf-8', xml_declaration=True)

