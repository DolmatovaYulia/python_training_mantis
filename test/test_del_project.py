from model.project import Project
import random


def test_del_project(app):
    if app.project.count() == 0:
        app.project.Create(Project(name="test"))
    old_projects = app.project.get_projects_list()
    project = random.choice(old_projects)
    app.project.Delete_by_id(project)
    new_projects = app.project.get_projects_list()
    assert len(old_projects) - 1 == len(new_projects)
    old_projects.remove(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)

