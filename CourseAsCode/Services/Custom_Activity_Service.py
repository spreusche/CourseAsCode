from abc import abstractmethod


class Custom_Activity_Service:

    @staticmethod
    @abstractmethod
    def generate_xmls(act_directory, act):
        pass

    @staticmethod
    @abstractmethod
    def create_activity(assignment_path, id, section_id, config):
        pass
