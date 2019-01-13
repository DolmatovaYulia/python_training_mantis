# Библиотека для получения почты
import poplib
# Библиотека для анализа текста
import email
import time


class MailHelper:
    def __init__(self, app):
        self.app = app

    def get_mail(self, username, password, subject):
        for i in range(5):
            # Устанавливаем соединение с сервером
            pop = poplib.POP3(self.app.config['james']['host'])
            # Указываем с каким именем и паролем нужно открыть сессию
            pop.user(username)
            pop.pass_(password)
            # Определяем количество писем
            num = pop.stat()[0]
            if num > 0:
                for n in range(num):
                    # Получаем письмо, текст письма находится во 2 элементе картежа
                    msglines = pop.retr(n+1)
                    msgtext = "\n".join(map(lambda x: x.decode('utf-8'), msglines))
                    # Сообщение, в котором выделен заголовок и тескт самого письма
                    msg = email.message_from_string(msgtext)
                    if msg.get('Subject') == subject:
                        pop.dele(n+1)
                        pop.quit()
                        # Возвращаем тело письма
                        return msg.get_payload()
            pop.quit()
            time.sleep(3)
        return None

