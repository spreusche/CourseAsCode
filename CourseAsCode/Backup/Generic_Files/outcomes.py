import xml.etree.ElementTree as ET


def create_xml(backup_dir):
    # Create a new XML tree
    outcomes_definition = ET.Element("outcomes_definition")

    tree = ET.ElementTree(outcomes_definition)
    tree.write(backup_dir + "/outcomes.xml", encoding='utf-8', xml_declaration=True)

