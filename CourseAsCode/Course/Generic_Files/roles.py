import xml.etree.ElementTree as ET
from CourseAsCode.Utils import Tag_Creator


def create_xml(course_dir):
    # Create a new XML tree
    roles = ET.Element("roles")
    #roles.text = '\n\t'

    Tag_Creator.create_tag(roles, "role_overrides", "", [])
    Tag_Creator.create_tag(roles, "role_assignments", "", [])

    tree = ET.ElementTree(roles)
    tree.write(course_dir + "/roles.xml", encoding='utf-8', xml_declaration=True)
