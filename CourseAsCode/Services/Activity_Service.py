import xml.etree.ElementTree as ET

from CourseAsCode.Models import Quiz
from CourseAsCode.Models.Activity import Activity


class Activity_Service:

    @staticmethod
    def create_activity(moduleid, sectionid, modulename, title, directory, text):
        return Activity(moduleid, sectionid, modulename, title, directory, text)

    @staticmethod
    def calendar_xml(act_directory):
        # Create a new XML tree
        events = ET.Element("events")

        tree = ET.ElementTree(events)
        tree.write(act_directory + "/calendar.xml", encoding='utf-8', xml_declaration=True)


    @staticmethod
    def filters_xml(act_directory):
        # Create a new XML tree
        filters = ET.Element("filters")
        # filters.text = '\n'

        # Create an element with some text
        filter_actives = ET.SubElement(filters, "filter_actives")
        # filter_actives.text = ''
        filter_actives.tail = "\n"
        filter_configs = ET.SubElement(filters, "filter_configs")
        # filter_configs.text = ''
        filter_configs.tail = "\n"

        # Create a new XML file and write the tree to it
        tree = ET.ElementTree(filters)
        tree.write(act_directory + "/filters.xml", encoding='utf-8', xml_declaration=True)

    @staticmethod
    def grade_history_xml(act_directory):
        # Create a new XML tree
        grade_history = ET.Element("grade_history")
        # grade_history.text = '\n'

        # Create an element with some text
        grade_grades = ET.SubElement(grade_history, "grade_grades")
        # grade_grades.text = ''
        grade_grades.tail = "\n"

        # Create a new XML file and write the tree to it
        tree = ET.ElementTree(grade_history)
        tree.write(act_directory + "/grade_history.xml", encoding='utf-8', xml_declaration=True)

    @staticmethod
    def grades_xml(act_directory):
        # Create a new XML tree
        activity_gradebook = ET.Element("activity_gradebook")
        # activity_gradebook.text = '\n'

        # Create an element with some text
        grade_items = ET.SubElement(activity_gradebook, "grade_items")
        # grade_items.text = ''
        grade_items.tail = "\n"
        grade_letters = ET.SubElement(activity_gradebook, "grade_letters")
        # grade_letters.text = ''
        grade_letters.tail = "\n"

        # Create a new XML file and write the tree to it
        tree = ET.ElementTree(activity_gradebook)
        tree.write(act_directory + "/grades.xml", encoding='utf-8', xml_declaration=True)


    @staticmethod
    def inforef_xml(act_directory):
        # Create a new XML tree
        inforef = ET.Element("inforef")

        tree = ET.ElementTree(inforef)
        tree.write(act_directory + "/inforef.xml", encoding='utf-8', xml_declaration=True)

    @staticmethod
    def roles_xml(act_directory):
        # Create a new XML tree
        roles_tag = ET.Element("roles")
        # roles_tag.text = '\n'

        # Create an element with some text
        role_overrides = ET.SubElement(roles_tag, "role_overrides")
        # role_overrides.text = ''
        role_overrides.tail = "\n"
        role_assignments = ET.SubElement(roles_tag, "role_assignments")
        # role_assignments.text = ''
        role_assignments.tail = "\n"


        # Create a new XML file and write the tree to it
        tree = ET.ElementTree(roles_tag)
        tree.write(act_directory + "/roles.xml", encoding='utf-8', xml_declaration=True)

    #TODO: override in quiz and future others that dont use it
    # also, be careful that ,aybe a page could have a file, so imforef should be considered
    @staticmethod
    def generate_activity_gen_files(act_directory):
        Activity_Service.calendar_xml(act_directory)
        Activity_Service.roles_xml(act_directory)
        Activity_Service.grades_xml(act_directory)
        Activity_Service.grade_history_xml(act_directory)
        Activity_Service.filters_xml(act_directory)
        Activity_Service.inforef_xml(act_directory)

