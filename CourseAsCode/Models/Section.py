class Section:
    def __init__(self, id, name, summary, sequence, directory):
        self.id = id
        self.name = name
        self.summary = summary
        self.sequence = sequence
        self.activities = {}            # Dict of the activities from this section
        self.number = id
        self.directory = directory
        self.files = []                 # List of all the files (pdf, png, etc...) from this section

    def __str__(self) -> str:
        return super().__str__()






