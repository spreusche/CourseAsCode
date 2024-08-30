import sys

import yaml

from CourseAsCode.Utils.Yaml_Object import Yaml_Object


def parse_yaml(yaml_file: str):
    with open(yaml_file, "r") as ymlfile:
        config = yaml.safe_load(ymlfile)

    ret = []
    section_id = 1
    activity_id = 1

    for sec in config['sections']:
        ret.append(Yaml_Object(sec['name'], "section", section_id, section_id, None))

        if 'activities' in sec:
            if sec['activities'] is not None:
                for act in sec['activities']:
                    if "config" in act:
                        ret.append(Yaml_Object(act['src'], act['type'], activity_id, section_id, act['config']))
                    else:
                        ret.append(Yaml_Object(act['src'], act['type'], activity_id, section_id, None))
                    activity_id += 1
        section_id += 1
    return ret


def get_section_number(yaml_elements: [], section_name: str):
    for element in yaml_elements:
        if element.type == 'section' and element.name == section_name:
            return element.id

    # raise Exception("section: " + section_name + " not found")
    print("Warning: section: " + section_name + " was not specified at sections.yaml")


def get_activity_number(yaml_elements: [], activity_name: str, type: str, section_id: int):
    for element in yaml_elements:
        if element.type == type and element.name == activity_name and element.section_id == section_id:
            return element.id

    # raise Exception("activity: " + activity_name + " of type: " + type + " not found")
    print("Warning: Activity:  " + activity_name + " of type: " + type + " was not specified at sections.yaml")


def get_yaml(yaml_file: str):
    with open(yaml_file, "r") as ymlfile:
        config = yaml.safe_load(ymlfile)
    return config


def get_config(yaml_elements: [], activity_name: str, type: str, section_id: int, configs: []):
    for element in yaml_elements:
        if element.type == type and element.name == activity_name and element.section_id == section_id:
            if element.config is not None:
                for c in configs:
                    if element.config == c.name:
                        return get_yaml(c.path)
    return []
