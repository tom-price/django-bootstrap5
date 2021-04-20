from bs4 import BeautifulSoup
from django import forms

from django_bootstrap5.exceptions import BootstrapError
from tests.base import BootstrapTestCase, TestForm


class FormTestForm(forms.Form):
    required_text = forms.CharField(required=True, help_text="<i>required_text_help</i>")
    optional_text = forms.CharField(required=False, help_text="<i>required_text_help</i>")


class BootstrapFormTestCase(BootstrapTestCase):
    def test_illegal_form(self):
        with self.assertRaises(BootstrapError):
            self.render("{% bootstrap_form form %}", {"form": "illegal"})

    def test_exclude(self):
        html = self.render('{% bootstrap_form form exclude="optional_text" %}', {"form": FormTestForm()})
        self.assertNotIn("optional_text", html)

    def test_error_class(self):
        form = TestForm({"optional_text": "my_message"})

        html = self.render("{% bootstrap_form form %}", {"form": form})
        self.assertIn("django_bootstrap5-err", html)

        html = self.render('{% bootstrap_form form error_css_class="custom-error-class" %}', {"form": form})
        self.assertIn("custom-error-class", html)

        html = self.render('{% bootstrap_form form error_css_class="" %}', {"form": form})
        self.assertNotIn("django_bootstrap5-err", html)

    def test_required_class(self):
        form = TestForm({"sender": "sender"})
        html = self.render("{% bootstrap_form form %}", {"form": form})
        self.assertIn("django_bootstrap5-req", html)

        html = self.render('{% bootstrap_form form required_css_class="custom-required-class" %}', {"form": form})
        self.assertIn("custom-required-class", html)

        html = self.render('{% bootstrap_form form required_css_class="" %}', {"form": form})
        self.assertNotIn("django_bootstrap5-req", html)

    def test_bound_class(self):
        form = TestForm({"sender": "sender"})

        html = self.render("{% bootstrap_form form %}", {"form": form})
        self.assertIn("django_bootstrap5-bound", html)

        form = TestForm({"sender": "sender"})

        html = self.render('{% bootstrap_form form bound_css_class="successful-test" %}', {"form": form})
        self.assertIn("successful-test", html)

        form = TestForm({"sender": "sender"})

        html = self.render('{% bootstrap_form form bound_css_class="" %}', {"form": form})
        self.assertNotIn("django_bootstrap5-bound", html)

    def test_alert_error_type(self):
        form = TestForm({"sender": "sender"})

        html = self.render("{% bootstrap_form form alert_error_type='all' %}", {"form": form})
        soup = BeautifulSoup(html, "html.parser")
        errors = list(soup.select(".text-danger")[0].stripped_strings)
        self.assertIn(form.non_field_error_message, errors)
        self.assertIn("This field is required.", errors)

        html = self.render("{% bootstrap_form form alert_error_type='non_fields' %}", {"form": form})
        self.assertEqual(
            html,
            self.render("{% bootstrap_form form %}", {"form": form}),
            "Default behavior is not the same as showing non-field errors",
        )

        soup = BeautifulSoup(html, "html.parser")
        errors = list(soup.select(".text-danger")[0].stripped_strings)
        self.assertIn(form.non_field_error_message, errors)
        self.assertNotIn("This field is required.", errors)

        html = self.render("{% bootstrap_form form alert_error_type='fields' %}", {"form": form})
        soup = BeautifulSoup(html, "html.parser")
        errors = list(soup.select(".text-danger")[0].stripped_strings)
        self.assertNotIn(form.non_field_error_message, errors)
        self.assertIn("This field is required.", errors)

        html = self.render("{% bootstrap_form form alert_error_type='none' %}", {"form": form})
        soup = BeautifulSoup(html, "html.parser")
        self.assertFalse(soup.select(".text-danger"))
