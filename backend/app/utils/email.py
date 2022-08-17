from os.path import join
import smtplib
from typing import Dict

from settings import Settings

settings = Settings()


def get_email_template_by_name(template_name: str):
    with open(join(settings.email_templates_base_path,template_name), 'r') as template_file:
        data = template_file.read()
    template_file.close()
    return data


class Email:

    def __init__(self, subject: str, to: str, email_template: str = None,
                 email_html: str = None, email_variables: Dict[str, str] = None):
        if email_template is not None and email_html is not None:
            raise ValueError('Only one argument is possible: email_template or email_html')
        self.subject = subject
        self.content = email_template or email_html
        self.email_variables = email_variables
        self.to = to

    def populate_variables(self):
        if self.email_variables:
            for key, value in self.email_variables.items():
                self.content = self.content.replace(f'{{{{{key}}}}}', value)

    def get_content(self):
        self.populate_variables()
        return self.content


class EmailSender:

    @staticmethod
    def send(email: Email):
        try:
            if settings.email_use_tls:
                server = smtplib.SMTP_SSL()
                server.login(settings.email_from, settings.email_password)
            else:
                server = smtplib.SMTP(host=settings.email_host, port=settings.email_port)
            server.ehlo()
            server.sendmail(settings.email_from, email.to, email.get_content())
            server.close()
            print('Email sent!')
        except Exception as exception:
            raise exception
