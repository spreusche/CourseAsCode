import hashlib
from os import DirEntry


def get_hash(file: DirEntry):
    hasher = hashlib.sha1()
    with open(file.path, "rb") as f:
        file_data = f.read()
    hasher.update(file_data)
    hex_digest = hasher.hexdigest()

    return hex_digest


class File:
    def __init__(self, file: DirEntry, file_id, section_id, file_area, component, config):
        self.module_id = file_id
        self.content_hash = get_hash(file)
        self.context_id = file_id  # Originally you can have multiple files for each context. But to simplify we will have all different contexts. <sortorder> is the responsible for showing these in case you need it.
        self.component = component
        self.area = file_area
        self.item_id = section_id
        self.path = "/"
        self.name = file.name
        self.user_id = "1"  # todo: not sure what this stands for
        self.size = file.stat().st_size
        self.type = file.name.split(".")[1]
        self.file = file
        self.directory = "activities/resource_" + str(self.module_id)
        self.link = "$@RESOURCEVIEWBYID*" + str(self.module_id) + "@$"
        self.module_name = "resource"
        self.config = config

