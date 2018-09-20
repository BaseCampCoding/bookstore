from urllib.parse import urlparse

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse, resolve

from selenium.webdriver import Firefox

class SeleniumTest(StaticLiveServerTestCase):
    serialized_rollback = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = Firefox()
        cls.browser.implicitly_wait(2)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def goto(self, viewname):
        self.browser.get(self.live_server_url + reverse(viewname))

    def link_to(self, viewname):
        return self.browser.find_element_by_css_selector(f"a[href='{reverse(viewname)}']")

    def input(self, input_name, text):
        element = self.browser.find_element_by_css_selector(f"input[name='{input_name}']")
        element.send_keys(text)

    def submit(self, form_id):
        button = self.browser.find_element_by_css_selector(f"#{form_id} button[type='submit']")
        button.click()

    @property
    def h1(self):
        return self.browser.find_element_by_tag_name('h1')

    @property
    def current_view(self):
        path = urlparse(self.browser.current_url).path
        match = resolve(path)
        return match.view_name


class TestUserCanNavigateToBookList(SeleniumTest):
    def test_it(self):
        self.goto('home')

        self.link_to('book-list').click()

        assert self.current_view == 'book-list'


class TestUserCanCreateAuthor(SeleniumTest):
    def test_it(self):
        self.goto('author-create')

        self.input('name', 'Nate')

        self.submit('author-create-form')

        assert self.current_view == 'author-detail'

        assert 'Nate' in self.h1.text

