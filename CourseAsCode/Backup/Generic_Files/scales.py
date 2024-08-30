import xml.etree.ElementTree as ET


def create_xml(backup_dir):
    # Create a new XML tree
    scales = ET.Element("scales_definition")

    tree = ET.ElementTree(scales)
    tree.write(backup_dir + "/scales.xml", encoding='utf-8', xml_declaration=True)
