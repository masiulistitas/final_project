# final_project
# Introduction
This is a simple Django notes app with registration. You can add notes, upload pictures and add categories.


# Getting Started
These instructions will give you a copy of the project up and running on your local machine for development and testing purposes.

### Installation process:
1. **On GitHub.com, navigate to the main page of the repository.**
2. **Above the list of files, click  Code.**

![](https://docs.github.com/assets/cb-20363/images/help/repository/code-button.png)

3. **Copy the URL for the repository.**
* To clone the repository using HTTPS, under "HTTPS", click.
* To clone the repository using an SSH key, including a certificate issued by your organization's SSH certificate authority, click SSH, then click.
* To clone a repository using GitHub CLI, click GitHub CLI, then click.
* Or you can download ZIP file of project.

![](https://docs.github.com/assets/cb-33207/images/help/repository/https-url-clone-cli.png)
4. **Open Git Bash.**
5. **Change the current working directory to the location where you want the cloned directory.**
6. **Type git clone, and then paste the URL you copied earlier.**

`$ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY`

7. **Press Enter to create your local clone.**

``Cloning into `django_individual_project`...
remote: Counting objects: 10, done.
remote: Compressing objects: 100% (8/8), done.
remove: Total 10 (delta 1), reused 10 (delta 1)
Unpacking objects: 100% (10/10), done.
``

### Creating Virtual Environment:

1. **Open the project Settings/Preferences and go to Project: project name | Python Interpreter.**
2. **Select Python Interpreter by clicking <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Ic_settings_48px.svg/2048px-Ic_settings_48px.svg.png" width="20" height="20"> button at the end and add.**
3. **Location should be specified correctly but please double check it.**
4. **Press OK.**
5. **Please open your terminal window and install requirements.txt file.**
`$ pip install -r requirements.txt`
6. **The project is ready for further development or testing.**
7. **This project is uploaded with migrations so you don't need to makemigration or migrate, just `$ python manage.py runserver` and enjoy!**




### Dependencies:
* asgiref==3.5.2
* Django==4.1.2
* django-bootstrap3==22.1
* Pillow==9.2.0
* sqlparse==0.4.3
* tzdata==2022.5


### Latest releases:
* Release 1.0
