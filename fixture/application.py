from selenium import webdriver
from fixture.session import SessionHelper
from fixture.project import ProjectHelper


# The class that contains all the helper methods.
class Application:
    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.wd.implicitly_wait(1)
        self.session = SessionHelper(self)
        self.project = ProjectHelper(self)
        self.base_url = base_url

    def Open_homepage(self):
        wd = self.wd
        if not (wd.current_url.endswith("http://addressbook/") and len(wd.find_elements_by_name("MassCB")) > 0):
            wd.get(self.base_url)

    def Destroy(self):
        self.wd.quit()

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except ():
            return False


