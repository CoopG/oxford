from operator import attrgetter
import os
from unittest import TestCase

from dpath import util
import yaml

from oxford.renderers import Search, Entry

BASE_DIR = 'tests'

with open(os.path.join(BASE_DIR, 'expected.yaml')) as f:
    EXPECTED = yaml.load(f)


class RendererMixin:
    field = None
    renderer = None

    def setUp(self):
        field = self.field

        with open(os.path.join(BASE_DIR, field + '.yaml')) as f:
            self.fields = list(map(self.renderer, yaml.load_all(f)))

        self.expected = EXPECTED[field]

    def assertLenEqual(self, glob, obj, exp):
        ag = attrgetter(glob)
        length = util.get(exp, glob, separator='.')['len']

        self.assertEqual(len(ag(obj)), length)

        return length


class SearchTests(RendererMixin, TestCase):
    field = 'searches'
    renderer = Search

    def test_renderer(self):
        for obj, exp in zip(self.fields, self.expected):
            self.assertLenEqual('result_set', obj, exp)
            self.assertLenEqual('result_set.fields', obj, exp)


class EntryTests(RendererMixin, TestCase):
    field = 'entries'
    renderer = Entry

    def test_renderer(self):
        for obj, exp in zip(self.fields, self.expected):
            self.assertLenEqual('lex_ents', obj, exp)

            for i, le in enumerate(obj.lex_ents):
                exp_le = exp['lex_ents'][i]
                self.assertLenEqual('example_sets', le, exp_le)
                self.assertLenEqual('translation_set.fields', le, exp_le)
