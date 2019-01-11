from model.project import Project
from selenium.webdriver.support.select import Select


class ProjectHelper:
    def __init__(self, app):
        self.app = app

    def Open_manage_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/manage_overview_page.php")):
            wd.find_element_by_link_text("Manage").click()

    def Open_project_page(self):
        wd = self.app.wd
        if not (wd.current_url.endswith("/manage_proj_page.php")):
            wd.find_element_by_link_text("Manage Projects").click()

    def Return_to_projects_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Proceed").click()

    def Create(self, group):
        wd = self.app.wd
        self.Open_manage_page()
        self.Open_project_page()
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        self.Fill_project_form(group)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        self.Return_to_projects_page()
        self.project_cache = None

    def Fill_project_form(self, project):
        wd = self.app.wd
        self.Change_field_value("name", project.name)
        self.Change_field_value_select("status", project.status)
        self.Change_field_value_checkbox("inherit_global", project.inherit_global)
        self.Change_field_value_select("view_state", project.view_state)
        self.Change_field_value("description", project.description)

    def Change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def Change_field_value_select(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            Select(wd.find_element_by_name(field_name)).select_by_visible_text(text)
            wd.find_element_by_name(field_name).click()

    def Change_field_value_checkbox(self, field_name, check):
        wd = self.app.wd
        if check is not None:
            wd.find_element_by_name(field_name).click()

    def count(self):
        wd = self.app.wd
        self.Open_manage_page()
        self.Open_project_page()
        return len(wd.find_elements_by_xpath("//tr[td/a[contains(@href, 'manage_proj_edit_page.php?project_id=')]]"))

    def Select_project_by_id(self, id):
        wd = self.app.wd
        wd.find_element_by_xpath("//a[contains(@href, 'manage_proj_edit_page.php?project_id=%s' )]" % id).click()

    def Delete_by_id(self, project):
        wd = self.app.wd
        self.Open_manage_page()
        self.Open_project_page()
        self.Select_project_by_id(project.id)
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        wd.find_element_by_css_selector("input[value='Delete Project']").click()
        self.project_cache = None

    project_cache = None

    def get_projects_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.Open_manage_page()
            self.Open_project_page()
            self.project_cache = []
            xpath = "//tr[td/a[contains(@href, 'manage_proj_edit_page.php?project_id=')]]"
            for element in wd.find_elements_by_xpath(xpath):
                cells = element.find_elements_by_xpath("td")
                name = cells[0].text
                status = cells[1].text
                if cells[2].text == 'X':
                    enabled = 'checked'
                else:
                    enabled = ''
                view_state = cells[3].text
                description = cells[4].text
                link_id = cells[0].find_element_by_xpath("a").get_attribute("href")
                id = link_id[link_id.find('id=') + 3:]
                self.project_cache.append(Project(name=name, status=status, inherit_global=enabled, view_state=view_state, description=description, id=id))
        return list(self.project_cache)
