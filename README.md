## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General information
An automatic tool for manager that assign tasks for their workers/team members.

## Detailed information
The program gets from the user input files with the tasks and the details of the workers.
The assignment is done in the most efficient wat after analyzation of these parameters: <br />
-The priority of the tasks. <br />
-The amount of the tasks.  <br />
-The allotted time of the tasks.  <br />
-The availability of the team members.  <br />
-The expertise of the team members.  <br />
In addition, Workers can login this tool and view their assigned tasks.  

	
## Technologies
Project is created with:
* Flask
* Sqlalchmy
* Pandas
* numpy
	
## Setup
In order to run this project:  <br />
git clone https://github.com/yaelhadad/FinalProject.git  <br />
cd Code  <br />
pip install flask flask_bootstrap wtforms flask_wtf flask_sqlalchemy flask_login werkzeug.security pandas numpy  <br />
python run.py  <br />