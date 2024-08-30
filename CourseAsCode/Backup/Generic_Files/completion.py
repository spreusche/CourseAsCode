import xml.etree.ElementTree as ET


def create_xml(backup_dir):
    # Create a new XML tree
    course_completion = ET.Element("course_completion")

    tree = ET.ElementTree(course_completion)
    tree.write(backup_dir + "/completion.xml", encoding='utf-8', xml_declaration=True)
