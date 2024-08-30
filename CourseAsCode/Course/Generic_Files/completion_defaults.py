import xml.etree.ElementTree as ET


def create_xml(course_dir):
    # Create a new XML tree
    completiondefaults = ET.Element("course_completion_defaults")

    tree = ET.ElementTree(completiondefaults)
    tree.write(course_dir + "/completiondefaults.xml", encoding='utf-8', xml_declaration=True)
