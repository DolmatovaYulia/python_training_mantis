from model.project import Project


def test_add_project(app, json_projects):
    project = json_projects
    old_projects = app.project.get_projects_list()
    app.project.Create(project)
    new_projects = app.project.get_projects_list()
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)

