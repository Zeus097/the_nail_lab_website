from django.test import TestCase
from services.forms import SearchForm

class TestSearchForm(TestCase):

    def test_valid_query(self):
        form = SearchForm(data={'query': 'Маникюр'})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['query'], 'Маникюр')

    def test_empty_query_is_valid(self):
        form = SearchForm(data={'query': ''})
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['query'], '')
