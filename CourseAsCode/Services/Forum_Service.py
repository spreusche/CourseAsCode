import sys
import time
from datetime import datetime

import yaml

from CourseAsCode.Models.Forum import Forum
from CourseAsCode.Utils import Tag_Creator
import xml.etree.ElementTree as ET


class Forum_Service:

    @staticmethod
    def forum_xml(act_directory, forum: Forum):
        tc = Tag_Creator
        activity_tag = ET.Element("activity")
        activity_tag.set("id", str(forum.module_id))
        activity_tag.set("moduleid", str(forum.module_id))
        activity_tag.set("modulename", "forum")
        activity_tag.set("contextid", str(12345))
        activity_tag.text = '\n\t'

        forum_tag = ET.SubElement(activity_tag, "forum")
        forum_tag.set("id", str(forum.module_id))

        tc.create_tag(forum_tag, "type", forum.type, [])
        tc.create_tag(forum_tag, "name", forum.title, [])
        tc.create_tag(forum_tag, "intro", forum.intro, [])
        tc.create_tag(forum_tag, "introformat", forum.introformat, [])
        tc.create_tag(forum_tag, "duedate", forum.duedate, [])
        tc.create_tag(forum_tag, "cutoffdate", forum.cutoffdate, [])
        tc.create_tag(forum_tag, "assessed", forum.assessed, [])
        tc.create_tag(forum_tag, "assesstimestart", forum.assesstimestart, [])
        tc.create_tag(forum_tag, "assesstimefinish", forum.assesstimefinish, [])
        tc.create_tag(forum_tag, "scale", forum.scale, [])
        tc.create_tag(forum_tag, "maxbytes", forum.maxbytes, [])
        tc.create_tag(forum_tag, "maxattachments", forum.maxattachments, [])
        tc.create_tag(forum_tag, "forcesubscribe", forum.forcesubscribe, [])
        tc.create_tag(forum_tag, "trackingtype", forum.trackingtype, [])
        tc.create_tag(forum_tag, "rsstype", forum.rsstype, [])
        tc.create_tag(forum_tag, "rssarticles", forum.rssarticles, [])
        tc.create_tag(forum_tag, "timemodified", str(int(time.time())), [])
        tc.create_tag(forum_tag, "warnafter", forum.warnafter, [])
        tc.create_tag(forum_tag, "blockafter", forum.blockafter, [])
        tc.create_tag(forum_tag, "blockperiod", forum.blockperiod, [])
        tc.create_tag(forum_tag, "completiondiscussions", forum.completiondiscussions, [])
        tc.create_tag(forum_tag, "completionreplies", forum.completionreplies, [])
        tc.create_tag(forum_tag, "completionposts", forum.completionposts, [])
        tc.create_tag(forum_tag, "displaywordcount", forum.displaywordcount, [])
        tc.create_tag(forum_tag, "lockdiscussionafter", forum.lockdiscussionafter, [])
        tc.create_tag(forum_tag, "grade_forum", forum.grade_forum, [])
        tc.create_tag(forum_tag, "discussions", "", [])
        tc.create_tag(forum_tag, "subscriptions", "", [])
        tc.create_tag(forum_tag, "digests", "", [])
        tc.create_tag(forum_tag, "readposts", "", [])
        tc.create_tag(forum_tag, "trackedprefs", "", [])
        tc.create_tag(forum_tag, "poststags", "", [])
        tc.create_tag(forum_tag, "grades", "", [])

        tree = ET.ElementTree(activity_tag)
        tree.write(act_directory + "/forum.xml", encoding='utf-8', xml_declaration=True)


    @staticmethod
    def parse_forum(name, forum_id, section_id, general_config):
        date_format = "%d-%m-%Y %H:%Mh"

        forum = Forum(forum_id, section_id, "forum", name, "activities/forum_" + str(forum_id), "", general_config)

        for att in general_config:
            match att:
                case "type":
                    forum.type = str(general_config["type"])
                case "introformat":
                    forum.introformat = str(general_config["introformat"])
                case "duedate":
                    if general_config["duedate"] != "0":
                        try:
                            date = str(int((datetime.strptime(general_config["duedate"], date_format)).timestamp()))
                            forum.duedate = date
                        except:
                            print("Forum duedate must follow the dd-mm-YYY hh:mm format")
                            sys.exit(1)
                    else:
                        forum.duedate = "0"
                case "cutoffdate":
                    if general_config["cutoffdate"] != "0":
                        try:
                            date = str(int((datetime.strptime(general_config["cutoffdate"], date_format)).timestamp()))
                            forum.cutoffdate = date
                        except:
                            print("Forum cutoffdate must follow the dd-mm-YYY hh:mm format")
                            sys.exit(1)
                    forum.cutoffdate = "0"
                case "assessed":
                    forum.assessed = str(general_config["assessed"])
                case "assesstimestart":
                    forum.assesstimestart = str(general_config["assesstimestart"])
                case "assesstimefinish":
                    forum.assesstimefinish = str(general_config["assesstimefinish"])
                case "scale":
                    forum.scale = str(general_config["scale"])
                case "maxbytes":
                    forum.maxbytes = str(general_config["maxbytes"])
                case "maxattachments":
                    forum.maxattachments = str(general_config["maxattachments"])
                case "forcesubscribe":
                    forum.forcesubscribe = str(general_config["forcesubscribe"])
                case "trackingtype":
                    forum.trackingtype = str(general_config["trackingtype"])
                case "rsstype":
                    forum.rsstype = str(general_config["rsstype"])
                case "rssarticles":
                    forum.rssarticles = str(general_config["rssarticles"])
                case "timemodified":
                    forum.timemodified = str(general_config["timemodified"])
                case "warnafter":
                    forum.warnafter = str(general_config["warnafter"])
                case "blockafter":
                    forum.blockafter = str(general_config["blockafter"])
                case "blockperiod":
                    forum.blockperiod = str(general_config["blockperiod"])
                case "completiondiscussions":
                    forum.completiondiscussions = str(general_config["completiondiscussions"])
                case "completionreplies":
                    forum.completionreplies = str(general_config["completionreplies"])
                case "completionposts":
                    forum.completionposts = str(general_config["completionposts"])
                case "displaywordcount":
                    forum.displaywordcount = str(general_config["displaywordcount"])
                case "lockdiscussionafter":
                    forum.lockdiscussionafter = str(general_config["lockdiscussionafter"])
                case "grade_forum":
                    forum.grade_forum = str(general_config["grade_forum"])

        return forum

    @staticmethod
    def comments_xml(act_directory):
        comments = ET.Element("comments")
        tree = ET.ElementTree(comments)
        tree.write(act_directory + "/comments.xml", encoding='utf-8', xml_declaration=True)

    @staticmethod
    def competencies_xml(act_directory):
        competencies_module = ET.Element("course_module_competencies")
        competencies = ET.SubElement(competencies_module, "competencies")

        tree = ET.ElementTree(competencies_module)
        tree.write(act_directory + "/competencies.xml", encoding='utf-8', xml_declaration=True)

    @staticmethod
    def completions_xml(act_directory):
        completions = ET.Element("completions")
        completionviews = ET.SubElement(completions, "completionviews")

        tree = ET.ElementTree(completions)
        tree.write(act_directory + "/completions.xml", encoding='utf-8', xml_declaration=True)

    @staticmethod
    def grading_xml(act_directory):
        tc = Tag_Creator
        areas = ET.Element("areas")
        area = ET.SubElement(areas, "area")
        area.set("id", "1")
        tc.create_tag(area, "areaname", "forum", [])
        tc.create_tag(area, "activemethod", "$@NULL@$", [])
        tc.create_tag(area, "definitions", "", [])

        tree = ET.ElementTree(areas)
        tree.write(act_directory + "/grading.xml", encoding='utf-8', xml_declaration=True)
