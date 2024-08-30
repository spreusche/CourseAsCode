import xml.etree.ElementTree as ET

from CourseAsCode.Models import Activity


class Grading_Service:
    @staticmethod
    def grades_xml(act_directory, act: Activity):
        activity_gradebook = ET.Element("activity_gradebook")
        grade_items = ET.SubElement(activity_gradebook, "grade_items")

        grade_item = ET.SubElement(grade_items, "grade_item")
        grade_item.set("id", str(act.module_id))
        grade_item.tail = '\n'

        categoryid = ET.SubElement(grade_item, "categoryid")
        categoryid.text = str(act.module_id)  # 41545 todo:
        categoryid.tail = '\n'

        itemname = ET.SubElement(grade_item, "itemname")
        itemname.text = act.name
        itemname.tail = '\n'

        itemtype = ET.SubElement(grade_item, "itemtype")
        itemtype.text = "mod"
        itemtype.tail = '\n'

        itemmodule = ET.SubElement(grade_item, "itemmodule")
        itemmodule.text = "quiz"
        itemmodule.tail = '\n'

        iteminstance = ET.SubElement(grade_item, "iteminstance")
        iteminstance.text = str(60671)  # 2 todo: id
        iteminstance.tail = '\n'

        itemnumber = ET.SubElement(grade_item, "itemnumber")
        itemnumber.text = str(0)
        itemnumber.tail = '\n'

        iteminfo = ET.SubElement(grade_item, "iteminfo")
        iteminfo.text = "$@NULL@$"
        iteminfo.tail = '\n'

        idnumber = ET.SubElement(grade_item, "idnumber")
        idnumber.tail = '\n'

        calculation = ET.SubElement(grade_item, "calculation")
        calculation.text = "$@NULL@$"
        calculation.tail = '\n'

        gradetype = ET.SubElement(grade_item, "gradetype")
        gradetype.text = str(1)
        gradetype.tail = '\n'

        grademax = ET.SubElement(grade_item, "grademax")
        grademax.text = str(10.00000)
        grademax.tail = '\n'

        grademin = ET.SubElement(grade_item, "grademin")
        grademin.text = str(0.00000)
        grademin.tail = '\n'

        scaleid = ET.SubElement(grade_item, "scaleid")
        scaleid.text = "$@NULL@$"
        scaleid.tail = '\n'

        outcomeid = ET.SubElement(grade_item, "outcomeid")
        outcomeid.text = "$@NULL@$"
        outcomeid.tail = '\n'

        gradepass = ET.SubElement(grade_item, "gradepass")
        gradepass.text = str(0.00000)
        gradepass.tail = '\n'

        multfactor = ET.SubElement(grade_item, "multfactor")
        multfactor.text = str(1.00000)
        multfactor.tail = '\n'

        plusfactor = ET.SubElement(grade_item, "plusfactor")
        plusfactor.text = str(0.00000)
        plusfactor.tail = '\n'

        aggregationcoef = ET.SubElement(grade_item, "aggregationcoef")
        aggregationcoef.text = str(0.00000)
        aggregationcoef.tail = '\n'

        aggregationcoef2 = ET.SubElement(grade_item, "aggregationcoef2")
        aggregationcoef2.text = str(1.00000)
        aggregationcoef2.tail = '\n'

        weightoverride = ET.SubElement(grade_item, "weightoverride")
        weightoverride.text = str(0)
        weightoverride.tail = '\n'

        sortorder = ET.SubElement(grade_item, "sortorder")
        sortorder.text = str(2)
        sortorder.tail = '\n'

        display = ET.SubElement(grade_item, "display")
        display.text = str(0)
        display.tail = '\n'

        decimals = ET.SubElement(grade_item, "decimals")
        decimals.text = "$@NULL@$"
        decimals.tail = '\n'

        hidden = ET.SubElement(grade_item, "hidden")
        hidden.text = str(1)
        hidden.tail = '\n'

        locked = ET.SubElement(grade_item, "locked")
        locked.text = str(0)
        locked.tail = '\n'

        locktime = ET.SubElement(grade_item, "locktime")
        locktime.text = str(0)
        locktime.tail = '\n'

        needsupdate = ET.SubElement(grade_item, "needsupdate")
        needsupdate.text = str(0)
        needsupdate.tail = '\n'

        timecreated = ET.SubElement(grade_item, "timecreated")
        timecreated.text = str(1688645726)
        timecreated.tail = '\n'

        timemodified = ET.SubElement(grade_item, "timemodified")
        timemodified.text = str(1688723921)
        timemodified.tail = '\n'

        grade_grades = ET.SubElement(grade_item, "grade_grades")
        grade_grades.tail = '\n'

        grade_letters = ET.SubElement(activity_gradebook, "grade_letters")
        grade_letters.tail = '\n'

        tree = ET.ElementTree(activity_gradebook)
        tree.write(act_directory + "/grades.xml", encoding='utf-8', xml_declaration=True)