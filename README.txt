# Nutribot Project Setup Guide

Welcome to my Final Year Project, Nutribot! A Django web app to help users plan meals and find recipies This guide will walk you through setting up the Nutribot Django application on your computer,Just follow these steps:

## Prerequisites

- **Python 3**: The project requires Python 3 to be installed on your machine. If you don't have Python installed, download and install it from [python.org](https://www.python.org/downloads/).
- **pip**: Ensure you have pip installed, which is Python's package manager. It usually comes with Python.

## Setup Instructions

### 1. Download and Extract the Project

You've likely already done this if you're reading this guide, but make sure my Nutribot project is downloaded and extracted to a folder on your laptop.

### 2. Open a Terminal or Command Prompt

Navigate to the project's directory using the terminal (on macOS or Linux) or command prompt (on Windows).

cd path/to/nutribot
Replace path/to/nutribot with the actual path where you extracted the Nutribot project.

3. Create a Virtual Environment (optional but I highly recomend it)
A virtual environment is a self-contained directory that contains a Python installation for a particular version of Python, plus a number of additional packages. This keeps dependencies required by different projects in separate places.


python3 -m venv myenv
To activate the virtual environment:

On macOS and Linux:
source myenv/bin/activate

On Windows:
cmd
myenv\Scripts\activate.bat

4. Install Required Dependencies
Install the project's required packages by running:

pip install -r requirements.txt

5. Run the Django Server.

python manage.py runserver
After running this command, you should see output indicating the server is running. You can then access the Nutribot application by going
to http://127.0.0.1:8000/ in your web browser. 
(I found that google chrome is the best browser to use so i highly recomend you use that for best results)

Next Steps
1.create an account and explore the Nutribot application in your web browser.

2.Review the new model.ipynb Jupyter notebook for insights into the project's machine learning model

3.you can create a new super user by runing this in terminal: python manage.py createsuperuser
but for simplicity you can use my admin user:
username:admin
password:admin

4.To view the database paste this link after running server and loging into admin account: http://127.0.0.1:8000/admin/