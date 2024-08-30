# CourseAsCode
## Introduction:
This project has the objective of creating courses for the Moodle Platform. These courses will be able to be imported from the restore function at the moodle site. 
With this project we are looking forward to find a more efficient way of creating courses giving the user the chance to have version control, and solve other issues that have negative effects on the creators
## Requirements:
* Python
* Libraries at requirements.txt
  * pip install -r requirements.txt

## Run:
After executing:   

`$> python main.py <course_path>`  

A file called 'CREATED_COURSE' will be created in the current working directory.
Open a terminal inside that directory and run the following command in order to create the .mbz file which will be used to restore the course from moodle:  

`$> tar -czvf <name>.mbz ./*` where <name> is just the name of the file.  

Once the mbz file is created go to https://moodle.technikum-wien.at/  
If an already created course will be replaced by the new one:
1) Go to the course page
2) Select 'More'
3) Select 'Course reuse'
4) Select 'Restore'
5) Drop the .mbz file inside 'Import backup file' and select 'restore'
6) Select 'continue'
7) Select 'Delete the contents of this course and then restore' and continue
   * If this does not work and admin permissions are enabled, select 'Restore as new course'
8) Select 'Next'
9) Check the box stating that course configurations will be overriden. And click 'next' until 'Perform restore'
10) Once is fully restored, the new course should be visible


## Creating your course
The file called 'courseExample' is a working example of a course.
It serves as a template to follow when creating the course.  
#### Note:
##### Names of folders and keys from configuration files, as well as the names of the configuration files (config.yaml, gradebook.yaml, order.yaml) MUST be the same as shown
##### File types MUST be followed  

Inside the root folder there must be 2 files (`config.yaml` and `sections.yaml`) and a Sections directory. 
- config.yaml: This is the configuration file. Coursename, start date, visibility, and so on will be stated here.
- sections.yaml: Is the order in which the course will be displayed. Divided by sections where each section has all of the activities
(files are also under activity tag). The names must be the exact names as in the respective directories including the file extension
  - Each of the activity entries has up to 3 values:
  1) type: refers to the module name
  2) src: refers to the activity file
  3) config: refers to the configuration for that activity (optional)
- Sections: contains all the directories that contain a section
- Configs: contains all the configurations that the activities could share.

Inside each of the section directories, there must be a new directory per type of activity (or one for Files).
These are: Assignments, Files, Labels, Pages, Quizzes, Forums.
Inside of each, all the activities from that type that are in that section may be added. 
## Be careful with file types
- Assignments and Forums: .yaml
- Files: any
- Labels and Pages: .md
- Quizzes: .json


## Adding new Activities:
There is a possibility to add support for new activities which are not already implemented.
In order to achieve this, the following steps must be followed:
- Create a service for the new activity:
  - The name must be [module_name]_Service.py where [module_name] is the new activity module name that is used (check the corresponding xml for reference)
  - Must implement Custom_Activity_Service which contains 2 abstract staticmethods:
    - create_activity(new_activity_path, id, section_id) : Activity -> This will create the activity
    - generate_xmls(act_directory, act: Activity) -> Here all xml files related to this activity will be generated
  - Add the service file to Services directory

- Create a Model for the new activity. It must extend Activity class. Add it to Models directory

- Within the new course directory, inside the desired section, add a new directory with the module name of the activity.
  - NOTE: Do not add it in plural as the others. Add by its module name only.


## Current limitations:
* Cannot repeat file names
* Do not attempt to create grades
* Grades aggregation works for the first category (fix in progress)
* Multiple choice and Coderunner questions
* Only the FHTW format is allowed (good opportunity for a possible project extension)