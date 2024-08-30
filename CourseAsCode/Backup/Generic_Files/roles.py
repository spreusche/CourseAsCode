import xml.etree.ElementTree as ET
from CourseAsCode.Utils import Tag_Creator


def create_xml(backup_dir):
    # Create a new XML tree
    roles_definition = ET.Element("roles_definition")
    #roles_definition.text = '\n\t'

    role = ET.Element("role")
    role.set("id", "5") #TODO: find out what is this 5. Probably nothing
    #role.text = '\n\t'

    Tag_Creator.create_tag(role, "name", "", [])
    Tag_Creator.create_tag(role, "shortname", "student", [])
    Tag_Creator.create_tag(role, "nameincourse", "$@NULL@$", [])
    Tag_Creator.create_tag(role, "description", "Some description", [])
    Tag_Creator.create_tag(role, "sortorder", "13", []) #TODO: hardcoded 13, find out what it is.
    Tag_Creator.create_tag(role, "archetype", "student", [])

    tree = ET.ElementTree(roles_definition)
    tree.write(backup_dir + "/roles.xml", encoding='utf-8', xml_declaration=True)

