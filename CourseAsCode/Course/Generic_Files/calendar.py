import xml.etree.ElementTree as ET


def create_xml(course_dir):
    # Create a new XML tree
    events = ET.Element("events")

    tree = ET.ElementTree(events)
    tree.write(course_dir + "/calendar.xml", encoding='utf-8', xml_declaration=True)

