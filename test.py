import unittest

from s3selectparser import s3_select_parser


class TestIntegration(unittest.TestCase):

    def test_select_all(self):
        parsed = s3_select_parser.parseString('SELECT * FROM S3Object')
        self.assertEqual(parsed.asDict(), {
            'select_list': ['*'],
            'table_name': ['S3Object'],
        })

    def test_select_asterisk(self):
        parsed = s3_select_parser.parseString('SELECT * FROM S3Object[*]')
        self.assertEqual(parsed.asDict(), {
            'select_list': ['*'],
            'table_name': ['S3Object'],
        })

    def test_select_with_alias(self):
        parsed = s3_select_parser.parseString(
            'SELECT a as my_alias_a, b my_alias_b, c FROM S3Object[*]')
        self.assertEqual(parsed.asDict(), {
            'select_list': [
                {'projection': 'a', 'column_alias': 'my_alias_a'},
                {'projection': 'b', 'column_alias': 'my_alias_b'},
                {'projection': 'c', 'column_alias': 'c'},
            ],
            'table_name': ['S3Object'],
        })
