from typing import Dict
from unittest import TestCase

from utils.email import EmailSender, Email, get_email_template_by_name


def email_factory(subject: str = None, to: str = None,
                  email_html: str = None, email_template: str = None,
                  email_variables: Dict[str, str] = None):
    if email_html or not email_template:
        return Email(subject=subject if subject else 'Hola Mundo',
                     to=to if to else 'test@app.com',
                     email_html=email_html if email_html else'<b>Primer mensaje<b>' )
    else:
        return Email(subject=subject if subject else 'Hola Mundo',
                     to=to if to else 'test@app.com',
                     email_template=email_template if email_template else '<b>First message with {{foo_variable}}<b>',
                     email_variables=email_variables if email_variables else {'foo_variable': 'foo_value'})


class TestSendEmail(TestCase):

    def test_send_email(self):
        email = email_factory()
        EmailSender.send(email)

    def test_send_email_no_to_assert_fails(self):
        email = email_factory()
        email.to = None
        with self.assertRaises(TypeError):
            EmailSender.send(email)

    def test_send_email_no_subject(self):
        email = email_factory()
        email.subject = None
        EmailSender.send(email)

    def test_send_email_no_body__assert_raise_error(self):
        email = email_factory()
        email.content = None
        with self.assertRaises(TypeError):
            EmailSender.send(email)


class TestEmail(TestCase):

    def test_create_email_with_html(self):
        fake_html = '<p>Hello World</p>'
        email = email_factory(email_html=fake_html)
        self.assertEqual(fake_html, email.content)
        self.assertEqual(fake_html, email.get_content())

    def test_create_email_with_template(self):
        fake_template = '<p>Hello {{name}}</p>'
        fake_variables = {'name': 'App'}
        expected_content = '<p>Hello App</p>'
        email = email_factory(email_template=fake_template, email_variables=fake_variables)
        self.assertEqual(expected_content, email.get_content())

    def test_create_email_with_html_and_template_assert_raises_exception(self):
        with self.assertRaises(ValueError):
            Email(to='as@as.com', subject='new email', email_template='asdasd', email_html='asdas')

    def test_read_email_templates_with_real_path(self):
        template_name = 'activate_account.html'
        template_content = get_email_template_by_name(template_name=template_name)
        self.assertIsNotNone(template_content)

    def test_read_email_templates_with_incorrect_path(self):
        template_name = 'fake_file_name.html'
        with self.assertRaises(FileNotFoundError):
            get_email_template_by_name(template_name=template_name)

