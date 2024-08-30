#Lets see what happens if i dont do it
#its not used, all values are null or 0
#i cant find any usage of this enrollments.xml file

import xml.etree.ElementTree as ET


def create_xml(course_dir):
    # Create a new XML tree
    enrolments = ET.Element("enrolments")
    enrols = ET.SubElement(enrolments, "enrols")
    enrols.tail = '\n'

    tree = ET.ElementTree(enrolments)
    tree.write(course_dir + "/enrolments.xml", encoding='utf-8', xml_declaration=True)

