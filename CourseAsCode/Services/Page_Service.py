import xml.etree.ElementTree as ET
import time

from CourseAsCode.Models.Activity import Activity


class Page_Service:
    @staticmethod
    def create_page_xml(act_directory, activity: Activity):
        # Create a new XML tree
        activity_tag = ET.Element("activity")
        activity_tag.set('id', str(activity.module_id))
        activity_tag.set('moduleid', str(activity.module_id))
        activity_tag.set('modulename', activity.module_name)
        activity_tag.set('contextid',
                         '12345')  # TODO: as stated in my pdf, this is something kind of weird. Refer to my document
        activity_tag.text = '\n\t'

        # <page>
        page = ET.SubElement(activity_tag, "page")
        page.set('id', '1')
        # page.text = '\n\t'
        page.tail = "\n"

        # <name>
        name = ET.SubElement(page, "name")
        name.text = activity.title
        name.tail = "\n\t"

        # <intro>
        intro = ET.SubElement(page, "intro")
        intro.text = ""
        intro.tail = "\n\t"

        # <introformat>
        introformat = ET.SubElement(page, "introformat")
        introformat.text = "1"
        introformat.tail = "\n\t"

        # <content>
        content = ET.SubElement(page, "content")
        content.text = activity.content
        content.tail = "\n\t"

        # <contentformat>
        contentformat = ET.SubElement(page, "contentformat")
        contentformat.text = "1"
        contentformat.tail = "\n\t"

        # Generic tags
        legacyfiles = ET.SubElement(page, "legacyfiles")
        legacyfiles.text = "1"
        legacyfiles.tail = "\n\t"
        legacyfileslast = ET.SubElement(page, "legacyfileslast")
        legacyfileslast.text = "$@NULL@$"
        legacyfileslast.tail = "\n\t"
        display = ET.SubElement(page, "display")
        display.text = "5"
        display.tail = "\n\t"
        displayoptions = ET.SubElement(page, "displayoptions")
        displayoptions.text = "a:3:{s:12:\"printheading\";s:1:\"1\";s:10:\"printintro\";s:1:\"1\";s:17:\"printlastmodified\";s:1:\"1\";}"
        displayoptions.tail = "\n\t"
        revision = ET.SubElement(page, "revision")
        revision.text = "1"
        revision.tail = "\n\t"
        timemodified = ET.SubElement(page, "timemodified")
        timemodified.text = str(int(time.time()))
        timemodified.tail = "\n"

        tree = ET.ElementTree(activity_tag)
        tree.write(act_directory + "/page.xml", encoding='utf-8', xml_declaration=True)
