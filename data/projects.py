from model.project import Project


testdata = [
    Project(name="name1", status="release", inherit_global="checked", view_state="private", description="test name"),
    Project(name="name2", status="stable", view_state="public", description="test name")
]