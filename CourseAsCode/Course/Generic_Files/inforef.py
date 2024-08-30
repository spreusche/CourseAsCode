# This seems to be in all courses, but the questions part does not
# todo: add the questions tag when the creator supports quizzes

# <inforef>
#   <roleref>
#     <role>
#       <id>5</id>
#     </role>
#   </roleref>

import xml.etree.ElementTree as ET
from CourseAsCode.Utils import Tag_Creator


def create_xml(course_dir, sections):
    # Create a new XML tree
    inforef = ET.Element("inforef")
    #inforef.text = '\n\t'

    roleref = ET.SubElement(inforef, "roleref")
    roleref.tail = '\n'

    Tag_Creator.create_tag(roleref, "role", "5", [])

    question_cat_ref = ET.SubElement(inforef, "question_categoryref")

    for sec in sections:
        if "Quiz" in sec.activities:
            for q in sec.activities["Quiz"]:
                question_category = ET.SubElement(question_cat_ref, "question_category")
                Tag_Creator.create_tag(question_category, "id", str(q.id), [])


    tree = ET.ElementTree(inforef)
    tree.write(course_dir + "/inforef.xml", encoding='utf-8', xml_declaration=True)
