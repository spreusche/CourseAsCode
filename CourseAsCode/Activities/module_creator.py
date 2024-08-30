import xml.etree.ElementTree as ET
import time


def create_xml(act_directory, module_id, module_name, section, config):
    module = ET.Element("module")
    module.set('id', str(module_id))
    module.set('version', '2021051700')

    module_name_tag = ET.SubElement(module, "modulename")
    module_name_tag.text = module_name
    module_name_tag.tail = '\n'

    section_id = ET.SubElement(module, "sectionid")
    section_id.text = str(section.id)
    section_id.tail = '\n'

    section_number = ET.SubElement(module, "sectionnumber")
    section_number.text = str(section.id)
    section_number.tail = '\n'

    id_number = ET.SubElement(module, "idnumber")
    id_number.tail = '\n'

    added = ET.SubElement(module, "added")
    added.text = str(int(time.time()))
    added.tail = '\n'

    # The following seem to be purely generic
    # TODO: check if any of these could be something that the user can change

    score = ET.SubElement(module, "score")
    if config is not None and "score" in config:
        score.text = str(config["score"])
    else:
        score.text = str(0)
    score.tail = '\n'

    indent = ET.SubElement(module, "indent")
    indent.text = str(0)
    indent.tail = '\n'

    visible = ET.SubElement(module, "visible")
    if config is not None and "visible" in config:
        visible.text = str(int(config["visible"] is True))
    else:
        visible.text = str(1)
    visible.tail = '\n'

    visibleoncoursepage = ET.SubElement(module, "visibleoncoursepage")
    if config is not None and "visibleoncoursepage" in config:
        visibleoncoursepage.text = str(int(config["visibleoncoursepage"] is True))
    else:
        visibleoncoursepage.text = str(1)
    visibleoncoursepage.tail = '\n'

    visibleold = ET.SubElement(module, "visibleold")
    if config is not None and "visibleold" in config:
        visibleold.text = str(int(config["visibleold"] is True))
    else:
        visibleold.text = str(1)
    visibleold.tail = '\n'

    groupmode = ET.SubElement(module, "groupmode")
    if module_name == "quiz":
        groupmode.text = str(2)
    else:
        groupmode.text = str(0)
    groupmode.tail = '\n'

    groupingid = ET.SubElement(module, "groupingid")
    groupingid.text = str(0)
    groupingid.tail = '\n'

    completion = ET.SubElement(module, "completion")
    completion.text = str(0)
    completion.tail = '\n'

    completiongradeitemnumber = ET.SubElement(module, "completiongradeitemnumber")
    completiongradeitemnumber.text = "$@NULL@$"
    completiongradeitemnumber.tail = '\n'

    completionview = ET.SubElement(module, "completionview")
    completionview.text = str(0)
    completionview.tail = '\n'

    completionexpected = ET.SubElement(module, "completionexpected")
    completionexpected.text = str(0)
    completionexpected.tail = '\n'

    availability = ET.SubElement(module, "availability")
    availability.text = "$@NULL@$"
    availability.tail = '\n'

    showdescription = ET.SubElement(module, "showdescription")
    if config is not None and "showdescription" in config:
        showdescription.text = str(int(config["showdescription"] is True))
    else:
        showdescription.text = str(0)
    showdescription.tail = '\n'

    plugin_plagiarism_turnitinsim_module = ET.SubElement(module, "plugin_plagiarism_turnitinsim_module")
    plugin_plagiarism_turnitinsim_module.tail = '\n'

    turnitinsim_mods = ET.SubElement(plugin_plagiarism_turnitinsim_module, "turnitinsim_mods")
    turnitinsim_mods.tail = '\n'

    tags = ET.SubElement(module, "tags")
    tags.tail = '\n'

    tree = ET.ElementTree(module)
    tree.write(act_directory + "/module.xml", encoding='utf-8', xml_declaration=True)






