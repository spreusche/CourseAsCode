import xml.etree.ElementTree as ET
import time

from CourseAsCode.Models.Section import Section
from CourseAsCode.Utils import Tag_Creator


def create_xml(sec_directory, section: Section):
    section_tag = ET.Element("section")
    section_tag.set("id", str(section.id))
    #section.text = '\n\t'

    number = ET.SubElement(section_tag, "number")
    number.text = str(section.number)
    number.tail = '\n'

    Tag_Creator.create_tag(section_tag, "name", section.name, [])

    summary = ET.SubElement(section_tag, "summary")
    summary.tail = '\n'

    summaryformat = ET.SubElement(section_tag, "summaryformat")
    summaryformat.text = str(1)
    summaryformat.tail = '\n'

    sequence = ET.SubElement(section_tag, "sequence")
    seq_txt_aux = ""
    sequence_arr = []
    # todo: sort acts with files so they are in the correct display order
    for module in section.activities:
        for act in section.activities[module]:
            sequence_arr.append(act.module_id)
    for f in section.files:
        sequence_arr.append(f.module_id)
    sequence_arr.sort()
    for n in sequence_arr:
        seq_txt_aux += str(n) + ","


    seq_txt_aux = seq_txt_aux[:-1]
    sequence.text = seq_txt_aux
    sequence.tail = '\n'

    visible = ET.SubElement(section_tag, "visible")
    visible.text = str(1)
    visible.tail = '\n'

    availabilityjson = ET.SubElement(section_tag, "availabilityjson")
    availabilityjson.text = "$@NULL@$"
    availabilityjson.tail = '\n'

    timemodified = ET.SubElement(section_tag, "timemodified")
    timemodified.text = str(int(time.time()))
    timemodified.tail = '\n'

    # TODO: check if these are necessary. The downloaded course from fhtw has them, but some do not.
    #  maybe it isnt necessary

    # These are not always the same 4 but different id's
    # cfo_1 = course_format_options_tag(section_tag, course_format_options_id, "", "blockname", "")
    # course_format_options_id += 1

    tree = ET.ElementTree(section_tag)
    tree.write(sec_directory + "/section.xml", encoding='utf-8', xml_declaration=True)

# def course_format_options_tag(section_tag: ET.Element, id, format, name, value):
#   cfo = ET.SubElement(section_tag, "course_format_options")
#   cfo.set("id", str(id))
#   format_tag = ET.SubElement(cfo, "format")
#   format_tag.text = format
#   format_tag.tail = '\n'
#   name_tag = ET.SubElement(cfo, "name")
#   name_tag.text = name
#   name_tag.tail = '\n'
#   value_tag = ET.SubElement(cfo, "value")
#   value_tag.text = str(value)
#   value_tag.tail = '\n'
#
#   return cfo


def create_inforef(sec_directory, files):
        # Create a new XML tree
        inforef = ET.Element("inforef")

        fileref = ET.SubElement(inforef, "fileref")
        for f in files:
            file = ET.SubElement(fileref, "file")
            id = ET.SubElement(file, "id")
            id.text = str(f.module_id)
            id.tail = '\n'

        tree = ET.ElementTree(inforef)
        tree.write(sec_directory + "/inforef.xml", encoding='utf-8', xml_declaration=True)

