class Activity:
    def __init__(self, moduleid, sectionid, modulename, title, directory, text, config):
        self.module_id = moduleid       #It is the ID also used in the <order> inside section
        self.section_id = sectionid     #Id corresponding to the section. (inside section.xml is called <number>)
        self.module_name = modulename
        self.title = title              #file name o ver como agarrar solo la linea del titulo inicial
        self.directory = directory      # activities/xxx_moduleid
        #self.filename
        self.intro = text               #TODO: def get_intro_from_text(text)
        self.content = text             #TODO: def get_content_from_text(text)
        self.files = []                 # todo: may not be being used. check usage
        self.config = config
