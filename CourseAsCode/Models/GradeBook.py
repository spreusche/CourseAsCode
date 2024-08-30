import time
import xml.etree.ElementTree as ET

from CourseAsCode.Utils import Tag_Creator


class GradeBook:

    def __init__(self, gradebook_yaml):
        keys = ["id",
                "aggregation",
                "type",
                "max",
                "min",
                "parentCat"]
        self.categories = []
        self.categories.append(Category("?", 1, 11, 1, 100.0, 0.0, "$@NULL@$"))  # course category
        if gradebook_yaml is None:
            return
        i = 0
        grade_type = 0
        aggregation = 0
        while i < len(gradebook_yaml["categories"]):
            for k in keys:
                if k not in gradebook_yaml["categories"][i]:
                   raise Exception("Missing fields at gradebook.yaml")
                else:
                    if not isinstance(gradebook_yaml["categories"][i]["category"], str):
                        raise ValueError("Category must be a string")
                    else:
                        name = gradebook_yaml["categories"][i]["category"]
                        if not isinstance(gradebook_yaml["categories"][i]["id"], int):
                            raise ValueError("id must be an integer")
                        else:
                            id = gradebook_yaml["categories"][i]["id"]

                        if not isinstance(gradebook_yaml["categories"][i]["aggregation"], str):
                            raise ValueError("aggregation must be an string")
                        else:
                            match gradebook_yaml["categories"][i]["aggregation"].lower():
                                case "mean":
                                    aggregation = 0
                                case "weighted mean":
                                    aggregation = 1
                                case "simple weighted":
                                    aggregation = 2
                                case "mean extra":
                                    aggregation = 3
                                case "median":
                                    aggregation = 4
                                case "lowest":
                                    aggregation = 5
                                case "highest":
                                    aggregation = 6
                                case "mode":
                                    aggregation = 7
                                case "natural":
                                    aggregation = 8

                        if not isinstance(gradebook_yaml["categories"][i]["type"], str):
                            raise ValueError("type must be an string")
                        else:

                            match gradebook_yaml["categories"][i]["type"].lower():
                                case "none":
                                    grade_type = 0
                                case "value":
                                    grade_type = 1
                                case "scale":
                                    grade_type = 2
                                case "text":
                                    grade_type = 3

                        if not isinstance(gradebook_yaml["categories"][i]["max"], int):
                            raise ValueError("max must be an integer")
                        else:
                            max = gradebook_yaml["categories"][i]["max"]

                        if not isinstance(gradebook_yaml["categories"][i]["min"], int):
                            raise ValueError("min must be an integer")
                        else:
                            min = gradebook_yaml["categories"][i]["min"]

                        if not isinstance(gradebook_yaml["categories"][i]["parentCat"], int):
                            raise ValueError("parentCat must be an integer")
                        else:
                            parentCat = gradebook_yaml["categories"][i]["parentCat"]
            i += 1

            # todo: check that the new category has a different id
            self.categories.append(Category(name, id, aggregation, grade_type, max, min, parentCat))

    def create_xml(self, course_creation_directory):
        tc = Tag_Creator
        depth = 1
        item = 1
        gradebook = ET.Element("gradebook")
        tc.create_tag(gradebook, "attributes", "", [])

        grade_categories = ET.SubElement(gradebook, "grade_categories")
        for c in self.categories:
            grade_category = ET.SubElement(grade_categories, "grade_category")
            grade_category.set("id", str(c.id))

            tc.create_tag(grade_category, "parent", str(c.parent), [])
            tc.create_tag(grade_category, "depth", str(depth), [])
            if c.parent == "$@NULL@$":
                tc.create_tag(grade_category, "path", "/" + str(c.id) + "/", [])
            else:
                tc.create_tag(grade_category, "path", "/" + str(c.parent) + "/" + str(c.id) + "/", [])
            tc.create_tag(grade_category, "fullname", c.name, [])
            tc.create_tag(grade_category, "aggregation", str(c.aggregation), [])
            tc.create_tag(grade_category, "keephigh", "0", [])
            tc.create_tag(grade_category, "droplow", "0", [])
            tc.create_tag(grade_category, "aggregateonlygraded", "1", [])
            tc.create_tag(grade_category, "aggregateoutcomes", "0", [])
            tc.create_tag(grade_category, "timecreated", str(int(time.time())), [])
            tc.create_tag(grade_category, "timemodified", str(int(time.time())), [])
            tc.create_tag(grade_category, "hidden", "0", [])
            depth += 1

        grade_items = ET.SubElement(gradebook, "grade_items")
        for c in self.categories:
            grade_item = ET.SubElement(grade_items, "grade_item")
            grade_item.set("id", str(item))

            tc.create_tag(grade_item, "categoryid", "$@NULL@$", [])
            tc.create_tag(grade_item, "itemname", "$@NULL@$", [])
            tc.create_tag(grade_item, "itemtype", "course", [])
            tc.create_tag(grade_item, "itemmodule", "$@NULL@$", [])
            tc.create_tag(grade_item, "iteminstance", str(c.id), [])
            tc.create_tag(grade_item, "itemnumber", "$@NULL@$", [])
            tc.create_tag(grade_item, "iteminfo", "$@NULL@$", [])
            tc.create_tag(grade_item, "idnumber", "$@NULL@$", [])
            tc.create_tag(grade_item, "calculation", "$@NULL@$", [])
            tc.create_tag(grade_item, "gradetype", str(c.type), [])
            tc.create_tag(grade_item, "grademax", str(c.max), [])
            tc.create_tag(grade_item, "grademin", str(c.min), [])
            tc.create_tag(grade_item, "scaleid", "$@NULL@$", [])
            tc.create_tag(grade_item, "outcomeid", "$@NULL@$", [])
            tc.create_tag(grade_item, "gradepass", str(0.00), []) # todo: ?
            tc.create_tag(grade_item, "multfactor", str(1.00), []) #
            tc.create_tag(grade_item, "plusfactor", str(0.00), []) #
            tc.create_tag(grade_item, "aggregationcoef", str(0.00), [])
            tc.create_tag(grade_item, "aggregationcoef2", str(0.00), [])
            tc.create_tag(grade_item, "weightoverride", str(0), [])
            tc.create_tag(grade_item, "sortorder", str(item), [])
            tc.create_tag(grade_item, "display", str(0), [])
            tc.create_tag(grade_item, "decimals", "$@NULL@$", [])
            tc.create_tag(grade_item, "hidden", str(0), [])
            tc.create_tag(grade_item, "locked", str(0), [])
            tc.create_tag(grade_item, "locktime", str(0), [])
            tc.create_tag(grade_item, "needsupdate", str(0), [])
            tc.create_tag(grade_item, "timecreated", str(int(time.time())), [])
            tc.create_tag(grade_item, "timemodified", str(int(time.time())), [])
            item += 1

        tc.create_tag(gradebook, "grade_letters", "", [])
        grade_settings = ET.SubElement(gradebook, "grade_settings")
        grade_setting = ET.SubElement(grade_settings, "grade_setting")
        grade_setting.set("id", "")
        tc.create_tag(grade_setting, "name", "minmaxtouse", [])
        tc.create_tag(grade_setting, "value", "1", [])

        tree = ET.ElementTree(gradebook)
        tree.write(course_creation_directory + "/gradebook.xml", encoding='utf-8', xml_declaration=True)





class Category:
    def __init__(self, name, id, aggregation, type, min, max, parent):
        self.name = name
        self.id = id
        self.aggregation = aggregation
        self.type = type
        self.min = min
        self.max = max
        self.parent = parent
