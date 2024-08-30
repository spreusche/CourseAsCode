import xml.etree.ElementTree as ET

#params = [(a,b)]
def create_tag(parent_tag, name, text, params):
    new_tag = ET.SubElement(parent_tag, name)
    if len(params) != 0:
        for key, value in params:
            new_tag.set(key, value)

    new_tag.text = text
    new_tag.tail = '\n'
