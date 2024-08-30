class Yaml_Object:
    def __init__(self, name, file_type, file_id, section_id, config):
        self.name = name  # src
        self.type = file_type
        self.id = file_id
        self.section_id = section_id
        self.config = config

    def __str__(self):
        return f"name = {self.name} - type = {self.type} - id = {self.id} - section_id = {self.section_id} - config = {self.config}"
