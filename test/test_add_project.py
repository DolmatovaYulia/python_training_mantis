from model.project import Project
import pytest


def test_add_project(app, json_projects):
    username = app.config['webadmin']['username']
    password = app.config['webadmin']['password']
    if not app.session.is_logged_in():
        app.session.Login(username, password)
    project = json_projects
    projects_list = app.project.get_projects_list()
    if len(list(filter(lambda x: x.name == project.name, projects_list))) > 0:
        pytest.skip("This project's name has been used - %s" % project.name)
    # old_projects = app.project.get_projects_list()
    old_projects = app.soap.get_user_projects(username, password)
    app.project.Create(project)
    # new_projects = app.project.get_projects_list()
    new_projects = app.soap.get_user_projects(username, password)
    assert len(old_projects) + 1 == len(new_projects)
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)
