#Lets see what happens if i dont do it
#its not used, all values are null or 0
#i cant find any usage of this enrollments.xml file

import xml.etree.ElementTree as ET
from CourseAsCode.Utils import Tag_Creator


def create_xml(course_dir):
    # Create a new XML tree
    filters = ET.Element("filters")
    actives = ET.SubElement(filters, "filter_actives")
    filters.tail = '\n'
    #TODO: please stop hardcoding stuff santi
    active = ET.SubElement(actives, "filter_active")

    Tag_Creator.create_tag(active, "filter", "activitynames", [])
    Tag_Creator.create_tag(active, "active", "-1", [])

    active2 = ET.SubElement(actives, "filter_active")

    Tag_Creator.create_tag(active2, "filter", "glossary", [])
    Tag_Creator.create_tag(active2, "active", "-1", [])

    active3 = ET.SubElement(actives, "filter_active")

    Tag_Creator.create_tag(active3, "filter", "sectionnames", [])
    Tag_Creator.create_tag(active3, "active", "1", [])

    tree = ET.ElementTree(filters)
    tree.write(course_dir + "/filters.xml", encoding='utf-8', xml_declaration=True)
