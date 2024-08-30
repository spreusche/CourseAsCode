import xml.etree.ElementTree as ET
from CourseAsCode.Utils import Tag_Creator


def create_xml(backup_dir):
    # Create a new XML tree
    groups = ET.Element("groups")
    #groups.text = '\n\t'

    Tag_Creator.create_tag(groups, "groupings", "", [])

    tree = ET.ElementTree(groups)
    tree.write(backup_dir + "/groups.xml", encoding='utf-8', xml_declaration=True)

