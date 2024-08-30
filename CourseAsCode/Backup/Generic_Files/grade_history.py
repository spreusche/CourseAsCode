import xml.etree.ElementTree as ET
from CourseAsCode.Utils import Tag_Creator


def create_xml(backup_dir):
    # Create a new XML tree
    grade_history = ET.Element("grade_history")
    #grade_history.text = '\n\t'

    Tag_Creator.create_tag(grade_history, "grade_grades", "", [])

    tree = ET.ElementTree(grade_history)
    tree.write(backup_dir + "/grade_history.xml", encoding='utf-8', xml_declaration=True)

