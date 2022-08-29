from os.path import join
import smtplib
from typing import Dict

from settings import Settings
from utils.errors import AppException

settings = Settings()


def get_email_template_by_name(template_name: str):
    for email_template_path in settings.email_templates_base_paths:
        try:
            with open(join(email_template_path, template_name), 'r') as template_file:
                data = template_file.read()
            template_file.close()
            return data
        except Exception:
            pass
    raise AppException(f'Email template {template_name} not found')


class Email:

    def __init__(self,
                 subject: str,
                 to: str,
                 email_template: str = None,
                 email_html: str = None,
                 email_variables: Dict[str, str] = None):
        if email_template is not None and email_html is not None:
            raise ValueError('Only one argument is possible: email_template or email_html')
        self.subject = subject
        if email_template:
            self.content = get_email_template_by_name(email_template)
        else:
            self.content = email_html
        self.email_variables = email_variables
        self.to = to

    def populate_variables(self):
        if self.email_variables and self.content:
            for key, value in self.email_variables.items():
                self.content = self.content.replace(f'{{{{{key}}}}}', value)

    def get_content(self):
        self.populate_variables()
        return f'Subject: {self.subject}\n\n{self.content if self.content else ""}'


class EmailSender:

    @staticmethod
    def send(email: Email):
        try:
            if settings.email_use_tls:
                server = smtplib.SMTP_SSL()
                server.login(settings.email_host_user, settings.email_host_password)
            else:
                server = smtplib.SMTP(host=settings.email_host, port=settings.email_port)
            server.ehlo()
            server.sendmail(from_addr=settings.email_from, to_addrs=email.to, msg=email.get_content())
            server.close()
        except Exception as exception:
            raise exception
