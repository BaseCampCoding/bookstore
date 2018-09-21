from app.templatetags import util
from django.test import SimpleTestCase
from django.http.request import QueryDict
from unittest.mock import MagicMock

class TestQueryParams(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.GET = QueryDict(mutable=True)
        cls.GET.update({'hello': 'world', 'game': 'over'})
        cls.context = MagicMock()
        cls.context.request.GET = cls.GET

    def test_query_params_preserves_existing_params(self):
        self.assertEqual(util.query_params(self.context), 'hello=world&game=over')

    def test_query_params_can_add_new_param(self):
        self.assertEqual(util.query_params(self.context,school='basecamp'), 'hello=world&game=over&school=basecamp')

    def test_query_params_can_replace_existing_param(self):
        self.assertEqual(util.query_params(self.context,hello='basecamp'), 'hello=basecamp&game=over')

