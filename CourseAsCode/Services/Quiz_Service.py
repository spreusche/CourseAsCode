import time

from CourseAsCode.Models import Quiz
from CourseAsCode.Models.Question import Question
from CourseAsCode.Models.Question_coderunner import Question_coderunner
from CourseAsCode.Models.Question_multichoice import Question_multichoice
from CourseAsCode.Models.Quiz import Quiz
from CourseAsCode.Models.Coderunner_test import Coderunner_test

from CourseAsCode.Services.Activity_Service import Activity_Service
import xml.etree.ElementTree as ET
import json

from CourseAsCode.Utils import Tag_Creator
from CourseAsCode.Utils.Config_utils import get_tag_config_date, get_tag_config, get_tag_config_boolean

answerid = 1


def category(question_categories_tag, name, category_id, context_level, ctxt_inst_id, quiz: Quiz):
    global answerid
    question_category = ET.SubElement(question_categories_tag, "question_category")
    question_category.set("id", str(category_id))

    name_tag = ET.SubElement(question_category, "name")
    name_tag.text = name
    name_tag.tail = '\n'

    contextid = ET.SubElement(question_category, "contextid")
    contextid.text = str(quiz.id)
    contextid.tail = '\n'

    contextlevel = ET.SubElement(question_category, "contextlevel")
    contextlevel.text = context_level
    contextlevel.tail = '\n'

    contextinstanceid = ET.SubElement(question_category, "contextinstanceid")
    contextinstanceid.text = ctxt_inst_id
    contextinstanceid.tail = '\n'

    info = ET.SubElement(question_category, "info")
    info.text = "The default category for questions shared in context " + "\'" + name + "\'"
    info.tail = '\n'

    infoformat = ET.SubElement(question_category, "infoformat")
    infoformat.text = str(0)
    infoformat.tail = '\n'

    stamp = ET.SubElement(question_category, "stamp")
    stamp.text = "moodle.technikum-wien.at+230706121530+sBqfWs"
    stamp.tail = '\n'

    parent = ET.SubElement(question_category, "parent")
    parent.text = str(
        1)  # cannot be 0, otherwise the system will consider it as a top category for the default category of the course and not even the admin can edit them
    parent.tail = '\n'

    sortorder = ET.SubElement(question_category, "sortorder")
    sortorder.text = str(0)
    sortorder.tail = '\n'

    idnumber = ET.SubElement(question_category, "idnumber")
    idnumber.text = "$@NULL@$"
    idnumber.tail = '\n'

    if len(quiz.questions) == 0:
        questions = ET.SubElement(question_category, "questions")
    else:
        questions = ET.SubElement(question_category, "questions")

        for q in quiz.questions:
            question = ET.SubElement(questions, "question")
            question.set("id", str(q.id) + str(quiz.id))

            qparent = ET.SubElement(question, "parent")
            qparent.text = "0"
            qparent.tail = '\n'

            qname = ET.SubElement(question, "name")
            qname.text = q.title
            qname.tail = '\n'

            questiontext = ET.SubElement(question, "questiontext")
            questiontext.text = q.text
            questiontext.tail = '\n'

            questiontextformat = ET.SubElement(question, "questiontextformat")
            questiontextformat.text = "1"
            questiontextformat.tail = '\n'

            generalfeedback = ET.SubElement(question, "generalfeedback")
            generalfeedback.text = q.feedback
            generalfeedback.tail = '\n'

            generalfeedbackformat = ET.SubElement(question, "generalfeedbackformat")
            generalfeedbackformat.text = "1"
            generalfeedbackformat.tail = '\n'

            defaultmark = ET.SubElement(question, "defaultmark")
            defaultmark.text = str(10.00000)
            defaultmark.tail = '\n'

            penalty = ET.SubElement(question, "penalty")
            penalty.text = str(0.33333)
            penalty.tail = '\n'

            qtype = ET.SubElement(question, "qtype")
            if q.type == 'multichoice':
                qtype.text = "oumultiresponse"
            elif q.type == 'coderunner':
                qtype.text = "coderunner"
            else:
                qtype.text = "essay"  # todo: this is why every other question is just considered an essay
            qtype.tail = '\n'

            length = ET.SubElement(question, "length")
            length.text = "1"
            length.tail = '\n'

            qstamp = ET.SubElement(question, "stamp")
            qstamp.text = "moodle.technikum-wien.at+230706121640+OTNCQb"
            qstamp.tail = '\n'

            version = ET.SubElement(question, "version")
            version.text = "moodle.technikum-wien.at+230707100022+m4o2ER"
            version.tail = '\n'

            hidden = ET.SubElement(question, "hidden")
            hidden.text = str(0)
            hidden.tail = '\n'

            timecreated = ET.SubElement(question, "timecreated")
            timecreated.text = str(int(time.time()))
            timecreated.tail = '\n'

            timemodified = ET.SubElement(question, "timemodified")
            timemodified.text = str(int(time.time()))
            timemodified.tail = '\n'

            createdby = ET.SubElement(question, "createdby")
            createdby.text = "31955"  # todo check ids in quizzes. this one is mine
            createdby.tail = '\n'

            modifiedby = ET.SubElement(question, "modifiedby")
            modifiedby.text = "31955"  # todo check ids in quizzes. this one is mine
            modifiedby.tail = '\n'

            idnumber = ET.SubElement(question, "idnumber")
            idnumber.text = "$@NULL@$"
            idnumber.tail = '\n'

            # todo: aca hacer que llame solo a un xml_creator, y que a partir del q.type lo decida de ese lado
            #   basicamente mover esta logica a otro lugar.
            match q.type.lower():
                case 'multichoice':
                    answerid = Quiz_Service.multichoice_xml(question, q, quiz, answerid)
                case 'coderunner':
                    Quiz_Service.coderunner_xml(question, q, quiz, answerid)


            # todo: have different tag creators for different plugins

            question_hints = ET.SubElement(question, "question_hints")
            question_hints.tail = '\n'

            tags = ET.SubElement(question, "tags")
            tags.tail = '\n'

    return question_category


class Quiz_Service:

    @staticmethod
    def create_quiz(moduleid, name, section_id, modulename, directory, text, config):
        return Quiz(moduleid, name, section_id, modulename, directory, text, config)

    @staticmethod
    def quiz_xml(act_directory, quiz: Quiz):
        activity_tag = ET.Element("activity")
        activity_tag.set("id", str(quiz.id))
        activity_tag.set("moduleid", str(quiz.id))
        activity_tag.set("modulename", "quiz")
        activity_tag.set("contextid", str(quiz.id))
        activity_tag.text = '\n\t'

        quiz_tag = ET.SubElement(activity_tag, "quiz")
        quiz_tag.set("id", str(quiz.id))

        name = ET.SubElement(quiz_tag, "name")
        name.text = quiz.name
        name.tail = '\n'

        intro = ET.SubElement(quiz_tag, "intro")
        intro.text = quiz.intro
        intro.tail = '\n'

        introformat = ET.SubElement(quiz_tag, "introformat")
        introformat.text = str(1)
        introformat.tail = '\n'

        timeopen = ET.SubElement(quiz_tag, "timeopen")
        timeopen.text = get_tag_config_date(quiz.config, "timeopen", str(0))
        timeopen.tail = '\n'

        timeclose = ET.SubElement(quiz_tag, "timeclose")
        timeclose.text = get_tag_config_date(quiz.config, "timeclose", str(0))
        timeclose.tail = '\n'

        timelimit = ET.SubElement(quiz_tag, "timelimit")
        timelimit.text = get_tag_config(quiz.config, "timelimit",
                                        str(0))
        timelimit.tail = '\n'

        overduehandling = ET.SubElement(quiz_tag, "overduehandling")
        overduehandling.text = get_tag_config(quiz.config, "overduehandling",
                                              "autosubmit")
        overduehandling.tail = '\n'

        graceperiod = ET.SubElement(quiz_tag, "graceperiod")
        graceperiod.text = get_tag_config(quiz.config, "graceperiod",
                                          str(0))
        graceperiod.tail = '\n'

        preferredbehaviour = ET.SubElement(quiz_tag, "preferredbehaviour")
        preferredbehaviour.text = get_tag_config(quiz.config, "preferredbehaviour",
                                                 "deferredfeedback")
        preferredbehaviour.tail = '\n'

        canredoquestions = ET.SubElement(quiz_tag, "canredoquestions")
        canredoquestions.text = get_tag_config_boolean(quiz.config, "canredoquestions", str(0))
        canredoquestions.tail = '\n'

        attempts_number = ET.SubElement(quiz_tag, "attempts_number")
        attempts_number.text = get_tag_config(quiz.config, "attempts_number", str(1))
        attempts_number.tail = '\n'

        attemptonlast = ET.SubElement(quiz_tag, "attemptonlast")
        attemptonlast.text = str(0)
        attemptonlast.tail = '\n'

        grademethod = ET.SubElement(quiz_tag, "grademethod")
        grademethod.text = str(1)
        grademethod.tail = '\n'

        decimalpoints = ET.SubElement(quiz_tag, "decimalpoints")
        decimalpoints.text = get_tag_config(quiz.config, "decimalpoints", str(2))
        decimalpoints.tail = '\n'

        questiondecimalpoints = ET.SubElement(quiz_tag, "questiondecimalpoints")
        questiondecimalpoints.text = str(-1)
        questiondecimalpoints.tail = '\n'

        reviewattempt = ET.SubElement(quiz_tag, "reviewattempt")
        reviewattempt.text = str(65535)
        reviewattempt.tail = '\n'

        reviewcorrectness = ET.SubElement(quiz_tag, "reviewcorrectness")
        reviewcorrectness.text = str(0)
        reviewcorrectness.tail = '\n'

        reviewmarks = ET.SubElement(quiz_tag, "reviewmarks")
        reviewmarks.text = str(0)
        reviewmarks.tail = '\n'

        reviewspecificfeedback = ET.SubElement(quiz_tag, "reviewspecificfeedback")
        reviewspecificfeedback.text = str(0)
        reviewspecificfeedback.tail = '\n'

        reviewgeneralfeedback = ET.SubElement(quiz_tag, "reviewgeneralfeedback")
        reviewgeneralfeedback.text = str(0)
        reviewgeneralfeedback.tail = '\n'

        reviewrightanswer = ET.SubElement(quiz_tag, "reviewrightanswer")
        reviewrightanswer.text = str(0)
        reviewrightanswer.tail = '\n'

        reviewoverallfeedback = ET.SubElement(quiz_tag, "reviewoverallfeedback")
        reviewoverallfeedback.text = str(0)
        reviewoverallfeedback.tail = '\n'

        questionsperpage = ET.SubElement(quiz_tag, "questionsperpage")
        questionsperpage.text = get_tag_config(quiz.config, "questionsperpage", str(1))
        questionsperpage.tail = '\n'

        navmethod = ET.SubElement(quiz_tag, "navmethod")
        navmethod.text = get_tag_config(quiz.config, "navmethod", "free")  # todo: find the other methods
        navmethod.tail = '\n'

        shuffleanswers = ET.SubElement(quiz_tag, "shuffleanswers")
        shuffleanswers.text = get_tag_config_boolean(quiz.config, "shuffleanswers", str(1))
        shuffleanswers.tail = '\n'

        sumgrades = ET.SubElement(quiz_tag, "sumgrades")
        sumgrades.text = get_tag_config(quiz.config, "sumgrades", str(1.00000))
        sumgrades.tail = '\n'

        grade = ET.SubElement(quiz_tag, "grade")
        grade.text = get_tag_config(quiz.config, "grade", str(10.00000))
        grade.tail = '\n'

        timecreated = ET.SubElement(quiz_tag, "timecreated")
        timecreated.text = str(time.time())
        timecreated.tail = '\n'

        timemodified = ET.SubElement(quiz_tag, "timemodified")
        timemodified.text = str(time.time())
        timemodified.tail = '\n'

        password = ET.SubElement(quiz_tag, "password")
        password.tail = '\n'

        subnet = ET.SubElement(quiz_tag, "subnet")
        subnet.tail = '\n'

        browsersecurity = ET.SubElement(quiz_tag, "browsersecurity")
        browsersecurity.text = "-"
        browsersecurity.tail = '\n'

        delay1 = ET.SubElement(quiz_tag, "delay1")
        delay1.text = str(0)
        delay1.tail = '\n'

        delay2 = ET.SubElement(quiz_tag, "delay2")
        delay2.text = str(0)
        delay2.tail = '\n'

        showuserpicture = ET.SubElement(quiz_tag, "showuserpicture")
        showuserpicture.text = str(0)
        showuserpicture.tail = '\n'

        showblocks = ET.SubElement(quiz_tag, "showblocks")
        showblocks.text = str(0)
        showblocks.tail = '\n'

        completionattemptsexhausted = ET.SubElement(quiz_tag, "completionattemptsexhausted")
        completionattemptsexhausted.text = str(0)
        completionattemptsexhausted.tail = '\n'

        completionpass = ET.SubElement(quiz_tag, "completionpass")
        completionpass.text = str(0)
        completionpass.tail = '\n'

        completionminattempts = ET.SubElement(quiz_tag, "completionminattempts")
        completionminattempts.text = str(0)
        completionminattempts.tail = '\n'

        allowofflineattempts = ET.SubElement(quiz_tag, "allowofflineattempts")
        allowofflineattempts.text = str(0)
        allowofflineattempts.tail = '\n'

        subplugin_quizaccess_honestycheck_quiz = ET.SubElement(quiz_tag, "subplugin_quizaccess_honestycheck_quiz")
        subplugin_quizaccess_honestycheck_quiz.tail = '\n'

        subplugin_quizaccess_ipaddresslist_quiz = ET.SubElement(quiz_tag, "subplugin_quizaccess_ipaddresslist_quiz")
        subplugin_quizaccess_ipaddresslist_quiz.tail = '\n'

        subplugin_quizaccess_safeexambrowser_quiz = ET.SubElement(quiz_tag, "subplugin_quizaccess_safeexambrowser_quiz")
        subplugin_quizaccess_safeexambrowser_quiz.tail = '\n'

        subplugin_quizaccess_seb_quiz = ET.SubElement(quiz_tag, "subplugin_quizaccess_seb_quiz")
        subplugin_quizaccess_seb_quiz.tail = '\n'

        question_instances = ET.SubElement(quiz_tag, "question_instances")
        slot = 1
        page = 1
        for question in quiz.questions:
            question_instance = ET.SubElement(question_instances, "question_instance")
            question_instance.set("id", str(question.id))  # I guess it's fine?

            slot_tag = ET.SubElement(question_instance, "slot")
            slot_tag.text = str(slot)
            slot_tag.tail = '\n'
            slot += 1

            page_tag = ET.SubElement(question_instance, "page")
            page_tag.text = str(page)
            page_tag.tail = '\n'
            page += 1

            requireprevious = ET.SubElement(question_instance, "requireprevious")
            requireprevious.text = str(0)
            requireprevious.tail = '\n'

            questionid = ET.SubElement(question_instance, "questionid")
            questionid.text = str(question.id) + str(quiz.id)
            questionid.tail = '\n'

            questioncategoryid = ET.SubElement(question_instance, "questioncategoryid")
            questioncategoryid.text = "$@NULL@$"
            questioncategoryid.tail = '\n'

            includingsubcategories = ET.SubElement(question_instance, "includingsubcategories")
            includingsubcategories.text = "$@NULL@$"
            includingsubcategories.tail = '\n'

            maxmark = ET.SubElement(question_instance, "maxmark")
            maxmark.text = str(1.0000000)
            maxmark.tail = '\n'

            tags = ET.SubElement(question_instance, "tags")
            tags.tail = '\n'

        # <sections>
        sections = ET.SubElement(quiz_tag, "sections")

        section_tag = ET.SubElement(sections, "section")
        section_tag.set("id", str(quiz.section_id))

        firstslot = ET.SubElement(section_tag, "firstslot")
        firstslot.text = str(1)
        firstslot.tail = '\n'

        heading = ET.SubElement(section_tag, "heading")
        heading.tail = '\n'

        shufflequestions = ET.SubElement(section_tag, "shufflequestions")
        shufflequestions.text = str(0)
        shufflequestions.tail = '\n'

        # <feedbacks>
        feedbacks = ET.SubElement(quiz_tag, "feedbacks")

        feedback = ET.SubElement(feedbacks, "feedback")
        feedback.set("id", str(quiz.section_id))  # TODO: i dont know what this feedback id stands for

        feedbacktext = ET.SubElement(feedbacks, "feedbacktext")
        feedbacktext.tail = '\n'

        feedbacktextformat = ET.SubElement(feedbacks, "feedbacktextformat")
        feedbacktextformat.text = str(1)
        feedbacktextformat.tail = '\n'

        mingrade = ET.SubElement(feedbacks, "mingrade")
        mingrade.text = str(0.00000)
        mingrade.tail = '\n'

        maxgrade = ET.SubElement(feedbacks, "maxgrade")  # todo: agregar el grade al quiz
        maxgrade.text = str(10.00000)
        maxgrade.tail = '\n'

        overrides = ET.SubElement(quiz_tag, "overrides")

        grades = ET.SubElement(quiz_tag, "grades")

        attempts = ET.SubElement(quiz_tag, "attempts")

        tree = ET.ElementTree(activity_tag)
        tree.write(act_directory + "/quiz.xml", encoding='utf-8', xml_declaration=True)


    @staticmethod
    def generate_quiz_gen_files(act_directory):
        Activity_Service.roles_xml(act_directory)
        Activity_Service.filters_xml(act_directory)
        Activity_Service.calendar_xml(act_directory)
        Activity_Service.grade_history_xml(act_directory)

    @staticmethod
    def inforef_xml(act_directory, quiz: Quiz):
        inforef = ET.Element("inforef")
        grade_itemref = ET.SubElement(inforef, "grade_itemref")
        grade_itemref.tail = '\n'
        grade_item = ET.SubElement(grade_itemref, "grade_item")
        grade_item.tail = '\n'
        id = ET.SubElement(grade_item, "id")
        id.text = str(quiz.id)  # todo: should be a real grade item id
        id.tail = '\n'

        tree = ET.ElementTree(inforef)
        tree.write(act_directory + "/inforef.xml", encoding='utf-8', xml_declaration=True)

    @staticmethod
    def questions_xml(course_directory, sections):
        ctxt_lvl = 50  # https://docs.moodle.org/dev/Roles_and_modules#:~:text=Context%20is%20an%20important%20concept,tuple%20%5Bcontextlevel%5D%5Binstanceid%5D.
        question_categories = ET.Element("question_categories")

        for sec in sections:
            if 'Quiz' in sec.activities:
                for quiz in sec.activities['Quiz']:
                    category(question_categories,
                             quiz.name,
                             str(quiz.id),
                             str(ctxt_lvl),
                             str(quiz.id), quiz)

        tree = ET.ElementTree(question_categories)
        tree.write(course_directory + "/questions.xml", encoding='utf-8', xml_declaration=True)

    @staticmethod
    def parse_quiz(quiz_path, quiz_id, section_id, last_question_created_id, config):
        last_question_created_id += 1  #
        with open(quiz_path) as quiz_json:
            data = json.load(quiz_json)
        name = data['name']
        intro = data['intro']
        questions = data['questions']

        quiz = Quiz(quiz_id, name, section_id, 'quiz', "activities/quiz_" + str(quiz_id), "", config)
        quiz.intro = intro

        for question in questions:
            match question['type']:
                case 'multichoice':
                    q = Question_multichoice(last_question_created_id,
                                             question['type'],
                                             question['title'],
                                             question['question'],
                                             question['feedback'])
                    q.correct = question['answers']['correct']
                    q.incorrect = question['answers']['wrong']

                case 'coderunner':
                    q = Question_coderunner(last_question_created_id,
                                            question['type'],
                                            question['title'],
                                            question['question'],
                                            question['feedback'])
                    q.coderunner_type = question['coderunnertype']
                    q.answer_preload = question['answerPreload']
                    q.answer = question['answer']
                    for test in question['tests']:
                        q.tests.append(Coderunner_test(test['testcode'], test['expected']))
                case _:
                    # todo: may throw error?
                    q = Question(last_question_created_id,
                                 question['type'],
                                 question['title'],
                                 question['question'],
                                 question['feedback'])
            quiz.questions.append(q)
            last_question_created_id += 1

        return quiz

    @staticmethod
    def multichoice_xml(parent_tag, question, quiz, answerid):
        plugin_qtype_oumultiresponse_question = ET.SubElement(parent_tag, "plugin_qtype_oumultiresponse_question")
        plugin_qtype_oumultiresponse_question.tail = '\n'

        answers = ET.SubElement(plugin_qtype_oumultiresponse_question, "answers")
        for a in question.incorrect:
            answer = ET.SubElement(answers, "answer")
            answer.set("id", str(answerid))
            answerid += 1

            answertext = ET.SubElement(answer, "answertext")
            answertext.text = a
            answertext.tail = '\n'

            answerformat = ET.SubElement(answer, "answerformat")
            answerformat.text = str(1)
            answerformat.tail = '\n'

            fraction = ET.SubElement(answer, "fraction")
            fraction.text = str(0.00000)
            fraction.tail = '\n'

            feedback = ET.SubElement(answer, "feedback")
            feedback.tail = '\n'

            feedbackformat = ET.SubElement(answer, "feedbackformat")
            feedbackformat.text = str(1)
            feedbackformat.tail = '\n'
        for a in question.correct:
            answer = ET.SubElement(answers, "answer")
            answer.set("id", str(answerid))
            answerid += 1

            answertext = ET.SubElement(answer, "answertext")
            answertext.text = a
            answertext.tail = '\n'

            answerformat = ET.SubElement(answer, "answerformat")
            answerformat.text = str(1)
            answerformat.tail = '\n'

            fraction = ET.SubElement(answer, "fraction")
            fraction.text = str(1.00000 / len(question.correct))
            fraction.tail = '\n'

            feedback = ET.SubElement(answer, "feedback")
            feedback.tail = '\n'

            feedbackformat = ET.SubElement(answer, "feedbackformat")
            feedbackformat.text = str(1)
            feedbackformat.tail = '\n'

        oumultiresponse = ET.SubElement(plugin_qtype_oumultiresponse_question, "oumultiresponse")
        oumultiresponse.set("id", str(quiz.id))
        oumultiresponse.tail = '\n'

        shuffleanswers = ET.SubElement(oumultiresponse, "shuffleanswers")
        shuffleanswers.text = str(1)
        shuffleanswers.tail = '\n'

        correctfeedback = ET.SubElement(oumultiresponse, "correctfeedback")
        correctfeedback.text = "Your answer is correct"
        correctfeedback.tail = '\n'

        correctfeedbackformat = ET.SubElement(oumultiresponse, "correctfeedbackformat")
        correctfeedbackformat.text = str(1)
        correctfeedbackformat.tail = '\n'

        partiallycorrectfeedback = ET.SubElement(oumultiresponse, "partiallycorrectfeedback")
        partiallycorrectfeedback.text = "Your answer is partially correct"
        partiallycorrectfeedback.tail = '\n'

        partiallycorrectfeedbackformat = ET.SubElement(oumultiresponse, "partiallycorrectfeedbackformat")
        partiallycorrectfeedbackformat.text = str(1)
        partiallycorrectfeedbackformat.tail = '\n'

        incorrectfeedback = ET.SubElement(oumultiresponse, "incorrectfeedback")
        incorrectfeedback.text = "Your answer is incorrect"
        incorrectfeedback.tail = '\n'

        incorrectfeedbackformat = ET.SubElement(oumultiresponse, "incorrectfeedbackformat")
        incorrectfeedbackformat.text = str(1)
        incorrectfeedbackformat.tail = '\n'

        answernumbering = ET.SubElement(oumultiresponse, "answernumbering")
        answernumbering.text = "abc"
        answernumbering.tail = '\n'

        shownumcorrect = ET.SubElement(oumultiresponse, "shownumcorrect")
        shownumcorrect.text = str(1)
        shownumcorrect.tail = '\n'

        showstandardinstruction = ET.SubElement(oumultiresponse, "showstandardinstruction")
        showstandardinstruction.text = str(0)
        showstandardinstruction.tail = '\n'

        return answerid

    @staticmethod
    def coderunner_xml(parent_tag, question, quiz, answerid):
        plugin_qtype_coderunner_question = ET.SubElement(parent_tag, "plugin_qtype_coderunner_question")
        coderunner_options = ET.SubElement(plugin_qtype_coderunner_question, "coderunner_options")

        coderunner_option = ET.SubElement(coderunner_options, "coderunner_option")
        coderunner_option.set("id", str(question.id))

        Tag_Creator.create_tag(coderunner_option, "coderunnertype", question.coderunner_type, [])
        Tag_Creator.create_tag(coderunner_option, "prototypetype", "0", [])
        Tag_Creator.create_tag(coderunner_option, "allornothing", "1", [])
        Tag_Creator.create_tag(coderunner_option, "penaltyregime", "10, 20, ...", [])
        Tag_Creator.create_tag(coderunner_option, "precheck", "0", [])
        Tag_Creator.create_tag(coderunner_option, "hidecheck", "0", [])
        Tag_Creator.create_tag(coderunner_option, "showsource", "0", [])
        Tag_Creator.create_tag(coderunner_option, "answerboxlines", "18", [])
        Tag_Creator.create_tag(coderunner_option, "answerboxcolumns", "100", [])
        Tag_Creator.create_tag(coderunner_option, "answerpreload",
                               question.answer_preload, [])
        Tag_Creator.create_tag(coderunner_option, "globalextra", "", [])
        Tag_Creator.create_tag(coderunner_option, "useace", "$@NULL@$", [])
        Tag_Creator.create_tag(coderunner_option, "resultcolumns", "$@NULL@$", [])
        Tag_Creator.create_tag(coderunner_option, "template", "$@NULL@$", [])
        Tag_Creator.create_tag(coderunner_option, "iscombinatortemplate", "$@NULL@$", [])
        Tag_Creator.create_tag(coderunner_option, "allowmultiplestdins", "$@NULL@$", [])
        Tag_Creator.create_tag(coderunner_option, "answer",
                               question.answer,
                               [])
        Tag_Creator.create_tag(coderunner_option, "validateonsave", "1", [])
        Tag_Creator.create_tag(coderunner_option, "testsplitterre", "$@NULL@$", [])
        Tag_Creator.create_tag(coderunner_option, "language", "$@NULL@$", [])
        Tag_Creator.create_tag(coderunner_option, "acelang", "$@NULL@$", [])
        Tag_Creator.create_tag(coderunner_option, "sandbox", "$@NULL@$", [])
        Tag_Creator.create_tag(coderunner_option, "grader", "$@NULL@$", [])
        Tag_Creator.create_tag(coderunner_option, "cputimelimitsecs", "$@NULL@$", [])
        Tag_Creator.create_tag(coderunner_option, "memlimitmb", "$@NULL@$", [])
        Tag_Creator.create_tag(coderunner_option, "sandboxparams", "$@NULL@$", [])
        Tag_Creator.create_tag(coderunner_option, "templateparams", "", [])
        Tag_Creator.create_tag(coderunner_option, "hoisttemplateparams", "1", [])
        Tag_Creator.create_tag(coderunner_option, "templateparamslang", "twig", [])
        Tag_Creator.create_tag(coderunner_option, "templateparamsevalpertry", "0", [])
        Tag_Creator.create_tag(coderunner_option, "templateparamsevald", "$@NULL@$", [])
        Tag_Creator.create_tag(coderunner_option, "twigall", "0", [])
        Tag_Creator.create_tag(coderunner_option, "uiplugin", "$@NULL@$", [])
        Tag_Creator.create_tag(coderunner_option, "uiparameters", "$@NULL@$", [])
        Tag_Creator.create_tag(coderunner_option, "attachments", "0", [])
        Tag_Creator.create_tag(coderunner_option, "attachmentsrequired", "0", [])
        Tag_Creator.create_tag(coderunner_option, "maxfilesize", "10240", [])
        Tag_Creator.create_tag(coderunner_option, "filenamesregex", "", [])
        Tag_Creator.create_tag(coderunner_option, "filenamesexplain", "", [])
        Tag_Creator.create_tag(coderunner_option, "displayfeedback", "1", [])
        Tag_Creator.create_tag(coderunner_option, "giveupallowed", "0", [])
        Tag_Creator.create_tag(coderunner_option, "prototypeextra", "$@NULL@$", [])

        # esto es un for con todos los tests...!
        Tag_Creator.create_tag(plugin_qtype_coderunner_question, "coderunner_testcases", "10240",
                               [])
        coderunner_testcases = ET.SubElement(plugin_qtype_coderunner_question, "coderunner_testcases")
        for test in question.tests:
            coderunner_testcase = ET.SubElement(coderunner_testcases, "coderunner_testcase")
            coderunner_testcase.set("id", str(question.id))

            Tag_Creator.create_tag(coderunner_testcase, "testcode", test.testcode, [])
            Tag_Creator.create_tag(coderunner_testcase, "testtype", "0", [])
            Tag_Creator.create_tag(coderunner_testcase, "expected", test.expected, [])
            Tag_Creator.create_tag(coderunner_testcase, "useasexample", "1", [])
            Tag_Creator.create_tag(coderunner_testcase, "display", "SHOW", [])
            Tag_Creator.create_tag(coderunner_testcase, "hiderestiffail", "0", [])
            Tag_Creator.create_tag(coderunner_testcase, "mark", "1.000", [])
            Tag_Creator.create_tag(coderunner_testcase, "stdin", "", [])
            Tag_Creator.create_tag(coderunner_testcase, "extra", "", [])

    # hacer metodo que agarre config, la config que quiero, el default y devuelva o el string de la config o el del default



