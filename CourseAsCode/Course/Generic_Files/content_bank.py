import xml.etree.ElementTree as ET


def create_xml(course_dir):
    # Create a new XML tree
    contents = ET.Element("contents")

    tree = ET.ElementTree(contents)
    tree.write(course_dir + "/contentbank.xml", encoding='utf-8', xml_declaration=True)
