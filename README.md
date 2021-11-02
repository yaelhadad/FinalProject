## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General information
An automatic tool for manager that assign tasks for their workers/team members.

## Detailed information
The program gets from the user input files with the tasks and the details of the workers.
The assignment is done in the most efficient wat after analyzation of these parameters:
-The priority of the tasks.
-The amount of the tasks.
-The allotted time of the tasks.
-The availability of the team members.
-The expertise of the team members.
In addition, Workers can login this tool and view their assigned tasks.


	
## Technologies
Project is created with:
* Flask
* Sqlalchmy
* Pandas
* numpy
	
## Setup
In order to run this project:
git clone https://github.com/yaelhadad/FinalProject.git
cd Code
pip install flask flask_bootstrap wtforms flask_wtf flask_sqlalchemy flask_login werkzeug.security pandas numpy
python run.py 