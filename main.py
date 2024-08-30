import shutil

from CourseAsCode.Activities import module_creator
from CourseAsCode.Models.Config import Config
from CourseAsCode.Models.File import File
from CourseAsCode.Models.GradeBook import GradeBook
from CourseAsCode.Models.Label import Label
from CourseAsCode.Models.Page import Page
from CourseAsCode.Sections import Section_files_creator
from CourseAsCode.Services.File_Service import File_Service
from CourseAsCode.Services.Forum_Service import Forum_Service
from CourseAsCode.Services.Generic_files_Service import Generic_files_Service
from CourseAsCode.Services.Grading_Service import Grading_Service
from CourseAsCode.Services.Label_Service import Label_Service
from CourseAsCode.Services.Page_Service import Page_Service
from CourseAsCode.Services.Quiz_Service import Quiz_Service
from CourseAsCode.Utils.href_modifier import href_to_activity
from CourseAsCode.Utils.md_to_html_parser import parse_md
from CourseAsCode.Utils.yaml_parser import parse_yaml, get_section_number, get_activity_number, get_yaml, get_config

from CourseAsCode.Models.Course import Course

from CourseAsCode.Course.Generic_Files import calendar as ccalendar, filters as cfilters, inforef as cinforef, roles as croles, \
    completion_defaults, content_bank
from CourseAsCode.Course import course

from CourseAsCode.Backup.Generic_Files import completion, grade_history as bgrade_history, groups, moodle_backup_log, outcomes, \
    roles as broles, scales
from CourseAsCode.Backup import files as bfiles, moodle_backup

import sys
import os
import importlib

from CourseAsCode.Models.Section import Section


course_creation_directory = "CREATED_COURSE"
activities_creation_directory = course_creation_directory + "/activities"
sections_creation_directory = course_creation_directory + "/sections"
course_created_directory = course_creation_directory + "/course"
files_creation_directory = course_creation_directory + "/files"

PAGE = "page"
PAGES = "pages"
LABEL = "label"
LABELS = "labels"
FORUM = "forum"
FORUMS = "forums"
QUIZ = "quiz"
QUIZZES = "quizzes"



services = {}


def create_full_course(new_course_dir):

    course_files = os.scandir(new_course_dir)
    sections_dir = None
    order_yaml = None
    config_yaml = None
    gradebook_yaml = None
    configs_dir = []

    # I get the service classes from Services
    services_dir = os.path.join("CourseAsCode", "Services")
    services_files = [f[:-3] for f in os.listdir(services_dir) if f.endswith(".py")]

    # File names must be same as class names
    for service_name in services_files:
        name = f"{services_dir.replace('/', '.')}.{service_name}"
        module = importlib.import_module(name)
        service = getattr(module, service_name)
        services[service_name.lower().split("_")[0]] = service

    for entry in course_files:
        if entry.name.lower() == 'sections' and entry.is_dir():
            sections_dir = os.scandir(new_course_dir + "/" + entry.name)
            sections_dir = [item for item in sections_dir if item.name != ".DS_Store"]
        else:
            if entry.name.lower() == 'configs' and entry.is_dir():
                configs_dir = os.scandir(new_course_dir + "/" + entry.name)
                configs_dir = [item for item in configs_dir if item.name != ".DS_Store"]

        # Must be named like this
        if entry.name == "sections.yaml":
            order_yaml = entry
        if entry.name == "config.yaml":
            config_yaml = entry
        if entry.name == "gradebook.yaml":
            gradebook_yaml = entry

    if order_yaml is None:
        raise Exception("sections.yaml file is missing")
    if config_yaml is None:
        raise Exception("config.yaml file is missing")

    if sections_dir is None:
        print("Empty courses are not supported. Please add at least 1 Section")
        sys.exit(1)

    yaml_elements = parse_yaml(new_course_dir + "/" + order_yaml.name)

    os.mkdir(course_creation_directory)
    os.mkdir(activities_creation_directory)
    os.mkdir(sections_creation_directory)
    os.mkdir(course_created_directory)
    files_directory = False

    sections = []  # list of sections
    configs = []

    for conf in configs_dir:
        configs.append(Config(conf))

    for section in sections_dir:
        current_section_number = get_section_number(yaml_elements, section.name)
        if current_section_number is None:
            continue
        os.mkdir(sections_creation_directory + "/section_" + str(current_section_number))

        this_section = Section(current_section_number,
                               section.name,
                               "f.read()",
                               None,
                               "sections/section_" +
                               str(current_section_number))

        # add in the activities folder each activity from the section
        folder_name = "Sections"
        current_section_path = os.path.join(new_course_dir, folder_name, section.name)
        current_section_files = os.scandir(current_section_path)
        last_question_created_id = 0
        if current_section_files is None:
            print("ERROR: Empty sections are not allowed on this version")
            sys.exit(1)
        for file in current_section_files:
            if file.is_dir():
                match file.name.lower():
                    case "pages" | "page":
                        file_activities = os.scandir(
                            current_section_path + "/" + file.name)  # I get the files inside new_course_dir/Sections/SectionName/Pages
                        for act in file_activities:
                            # act is the file of the activity
                            if act.name.split(".")[1] != "md":
                                raise Exception(act.name + " must be .md")
                            current_activity_id = get_activity_number(yaml_elements, act.name, 'page', current_section_number)
                            config = get_config(yaml_elements, act.name, PAGE, current_section_number, configs)
                            activity = Page(current_activity_id, current_section_number, PAGE, act.name,
                                            "activities/page_" + str(current_activity_id),
                                            parse_md(current_section_path + "/" + file.name + "/" + act.name),
                                            config
                                            )
                            if "Page" in this_section.activities:
                                this_section.activities["Page"].append(activity)
                            else:
                                this_section.activities["Page"] = [activity]

                    case "labels" | "label":
                        file_activities = os.scandir(
                            current_section_path + "/" + file.name)  # I get the files inside new_course_dir/Sections/SectionName/Labels
                        for act in file_activities:
                            # act is the file of the activity
                            if act.name.split(".")[1] != "md":
                                raise Exception(act.name + " must be .md")
                            current_activity_id = get_activity_number(yaml_elements, act.name, 'label', current_section_number)
                            if current_activity_id is not None:
                                config = get_config(yaml_elements, act.name, LABEL, current_section_number, configs)
                                activity = Label(current_activity_id, current_section_number, LABEL, act.name,
                                                 "activities/label_" + str(current_activity_id),
                                                 parse_md(current_section_path + "/" + file.name + "/" + act.name),
                                                 config
                                                 )
                                if "Label" in this_section.activities:
                                    this_section.activities["Label"].append(activity)
                                else:
                                    this_section.activities["Label"] = [activity]

                    case "files" | "file":
                        if not files_directory:
                            os.mkdir(files_creation_directory)
                            files_directory = True
                        files = os.scandir(
                            current_section_path + "/" + file.name)
                        for f in files:
                            if f.name != ".DS_Store":
                                current_filey_id = get_activity_number(yaml_elements, f.name, 'file', current_section_number)
                                config = get_config(yaml_elements, f.name, "file", current_section_number, configs)
                                current_file = File(f, current_filey_id,
                                                    current_section_number,
                                                    "content",
                                                    "mod_resource",
                                                    config)
                                this_section.files.append(current_file)
                                if "Resource" in this_section.activities:
                                    this_section.activities["Resource"].append(current_file)
                                else:
                                    this_section.activities["Resource"] = [current_file]

                    case "quizzes" | "quiz":
                        quizzes = os.scandir(current_section_path + "/" + file.name)
                        for q in quizzes:
                            if q.name.split(".")[1] != "json":
                                raise Exception(q.name + " must be .json")
                            current_quiz_id = get_activity_number(yaml_elements, q.name, 'quiz', current_section_number)
                            config = get_config(yaml_elements, q.name, "quiz", current_section_number, configs)
                            quiz = Quiz_Service.parse_quiz(q.path, current_quiz_id, current_section_number,
                                                           last_question_created_id, config)
                            last_question_created_id = quiz.last_question_id

                            if "Quiz" in this_section.activities:
                                this_section.activities["Quiz"].append(quiz)
                            else:
                                this_section.activities["Quiz"] = [quiz]

                    case "forums" | "forum":
                        forums = os.scandir(current_section_path + "/" + file.name)
                        for f in forums:
                            current_forum_id = get_activity_number(yaml_elements, f.name, 'forum', current_section_number)
                            if current_forum_id is not None:
                                config = get_config(yaml_elements, f.name, "forum", current_section_number, configs)
                                forum = Forum_Service.parse_forum(f.name.split(".")[0], current_forum_id, current_section_number, config)

                                if "Forum" in this_section.activities:
                                    this_section.activities["Forum"].append(forum)
                                else:
                                    this_section.activities["Forum"] = [forum]

                    # case "assignments":
                    #     assignments = os.scandir(current_section_path + "/" + file.name)
                    #     for a in assignments:
                    #         if a.name.split(".")[1] != "yaml":
                    #             raise Exception(a.name + " must be .yaml")
                    #         current_assign_id = get_activity_number(yaml_elements, a.name, 'assignment', current_section_number)
                    #         assignment = Assignment_Service.parse_assign(a.path,
                    #                                                      current_assign_id,
                    #                                                      current_section_number)
                    #
                    #         if "Assignment" in this_section.activities:
                    #             this_section.activities["Assignment"].append(assignment)
                    #         else:
                    #             this_section.activities["Assignment"] = [assignment]

                    # todo: for custom ones name directory as module name!!!!
                    #  PLEASE CHECK: that the module name you use is the one used in the backup xml you want to replicate
                    #   the custom model must extend from Activity!!!!
                    case _:
                        module_name = file.name.lower()
                        custom_service = services[module_name]
                        customs = os.scandir(current_section_path + "/" + file.name)

                        for c in customs:
                            current_custom_id = get_activity_number(yaml_elements, c.name, module_name,
                                                                    current_section_number)

                            # I send you the path to the activity you want to create, and you do what you must.
                            # todo: service must have a create_activity(path, id, setcion_id, config) method.!!!!!
                            #   must return the activity

                            config = get_config(yaml_elements, c.name, module_name, current_section_number, configs)
                            # config may be empty []
                            custom_activity = custom_service.create_activity(c.path,
                                                                             current_custom_id,
                                                                             current_section_number,
                                                                             config)

                            if module_name in this_section.activities:
                                this_section.activities[module_name].append(custom_activity)
                            else:
                                this_section.activities[module_name] = [custom_activity]

        sections.append(this_section)

    course_config = get_yaml(new_course_dir + "/" + config_yaml.name)
    gradebook = None
    if gradebook_yaml is not None:
        gb_yaml = get_yaml(new_course_dir + "/" + gradebook_yaml.name)
        gradebook = GradeBook(gb_yaml)
    create_activities_files(sections)
    create_sections_files(sections)
    c = Course("1", "1", sections, course_config)
    create_course_files(c)
    course.create_xml(course_created_directory, c)
    create_backup_files("myfirstcourse.mbz", c, gradebook)
    print("\nCourse has been successfully created at CREATED_COURSE!")


def create_activities_files(sections):
    for sec in sections:
        if len(sec.activities) != 0:
            for module in sec.activities:
                for act in sec.activities[module]:
                    act_directory = activities_creation_directory + "/" + act.module_name + "_" + str(act.module_id)
                    os.mkdir(act_directory)
                    module_creator.create_xml(act_directory, act.module_id, act.module_name, sec, act.config)
                    href_to_activity(act, sections)

                    match act.module_name.lower():
                        case "page":
                            generate_activity_gen_files(act_directory)
                            Page_Service.create_page_xml(act_directory, act)
                        case "label":
                            generate_activity_gen_files(act_directory)
                            Label_Service.create_label_xml(act_directory, act)
                        case "quiz":
                            Quiz_Service.generate_quiz_gen_files(act_directory)
                            Quiz_Service.inforef_xml(act_directory, act)
                            Grading_Service.grades_xml(act_directory, act)
                            Quiz_Service.quiz_xml(act_directory, act)
                        case "forum":
                            generate_activity_gen_files(act_directory)
                            Forum_Service.forum_xml(act_directory, act)
                            Forum_Service.grading_xml(act_directory)
                            Forum_Service.completions_xml(act_directory)
                            Forum_Service.competencies_xml(act_directory)
                            Forum_Service.comments_xml(act_directory)
                        case "resource":
                            # act is type File inside here
                            file_dir = files_creation_directory + "/" + act.content_hash[0:2]
                            if not os.path.exists(file_dir):
                                os.mkdir(file_dir)
                            new_file_path = os.path.join(file_dir + "/", act.content_hash)
                            shutil.copy(act.file, new_file_path)
                            File_Service.generate_activity_gen_files(act_directory)
                            File_Service.inforef_xml(act, act_directory)
                            File_Service.resource_xml(act_directory, act)
                        # case "assign":
                        #     Assignment_Service.assign_gen_files(act_directory)
                        #     Assignment_Service.assign_xml(act_directory, act)
                        #     Grading_Service.grades_xml(act_directory, act)
                        case _:
                            custom_service = services[act.module_name.lower()]
                            # todo: custom service must have a generate_xmls(directory, activity) method!!!!
                            custom_service.generate_xmls(act_directory, act)


def create_sections_files(sections):
    for sec in sections:
        sec_directory = sections_creation_directory + "/section_" + str(sec.id)
        Section_files_creator.create_inforef(sec_directory, sec.files)
        Section_files_creator.create_xml(sec_directory, sec)


def create_course_files(course):
    ccalendar.create_xml(course_created_directory)
    completion_defaults.create_xml(course_created_directory)
    content_bank.create_xml(course_created_directory)
    cinforef.create_xml(course_created_directory, course.sections)
    cfilters.create_xml(course_created_directory)
    croles.create_xml(course_created_directory)


def create_backup_files(filename, c: Course, gradebook: GradeBook):
    completion.create_xml(course_creation_directory)
    bgrade_history.create_xml(course_creation_directory)
    groups.create_xml(course_creation_directory)
    moodle_backup_log.create_log(course_creation_directory)
    outcomes.create_xml(course_creation_directory)
    broles.create_xml(course_creation_directory)
    scales.create_xml(course_creation_directory)
    bfiles.create_xml(course_creation_directory, c.sections)
    if gradebook is not None:
        gradebook.create_xml(course_creation_directory)
    moodle_backup.create_xml(course_creation_directory, filename, c)  # the main one
    Quiz_Service.questions_xml(course_creation_directory, c.sections)


# all these are generic files inside each activity
def generate_activity_gen_files(act_directory):
    gfs = Generic_files_Service()
    gfs.create_roles_xml(act_directory)
    gfs.create_calendar_xml(act_directory)
    gfs.create_grades_xml(act_directory)
    gfs.create_grade_hist_xml(act_directory)
    gfs.create_filters_xml(act_directory)
    gfs.create_inforef_xml(act_directory)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python main.py <\"your_course_directory\">")
        sys.exit(1)
    course_dir = sys.argv[1]
    create_full_course(course_dir)
