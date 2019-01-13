from suds.client import Client
from suds import WebFault
from model.project import Project


class SoapHelper:
    def __init__(self, app):
        self.app = app

    # Проверка, что пользователь может войти в систему
    def can_login(self, username, password):
        # Делаем запрос о веб-сервисе
        client = Client("http://mantisbt/api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_user_projects(self, username, password):
        client = Client("http://mantisbt/api/soap/mantisconnect.php?wsdl")
        project_list = []
        try:
            soap_list = client.service.mc_projects_get_user_accessible(username, password)
            for element in soap_list:
                project_list.append(Project(name=element.name, status=element.status, inherit_global=element.enabled, view_state=element.view_state, description=element.description, id=str(element.id)))
            return project_list
        except WebFault:
            return False

