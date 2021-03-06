#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from pyxform.tests_v1.pyxform_test_case import PyxformTestCase


class UnicodeStrings(PyxformTestCase):
    def test_unicode_snowman(self):
        self.assertPyxformXform(
            md="""
            | survey |      |         |       |
            |        | type | name    | label |
            |        | text | snowman | ☃     |
            """,
            errored=False,
            xml__contains=[
                '<label>☃</label>',
            ],
        )

    def test_smart_quotes(self):
        self.assertPyxformXform(
            ss_structure={
                'survey': [
                    {'type': 'select_one xyz',
                     'name': 'smart_single_quoted',
                     'label': u'''
                     ‘single-quoted’
                     '''.strip()},
                    {'type': 'text',
                     'name': 'smart_double_quoted',
                     'relevant': 'selected(${smart_single_quoted}, ‘xxx’)',
                     'label': u'''
                     “double-quoted”
                     '''.strip()},
                ],
                'choices': [
                    {'list_name': 'xyz',
                     'name': 'xxx',
                     'label': '‘Xxx’'},
                    {'list_name': 'xyz',
                     'name': 'yyy',
                     'label': '“Yyy”'},
                ],
                'settings': [{'version': 'q(‘-’)p'}],
            },
            errored=False,
            validate=False,
            name="quoth",
            xml__contains=[
                "'single-quoted",
                '"double-quoted"',
                "selected( /quoth/smart_single_quoted , 'xxx')",
                "<label>'Xxx'</label>",
                '<label>"Yyy"</label>',
                '''
                version="q('-')p"
                '''.strip(),
            ],
        )
