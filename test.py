import unittest

from s3selectparser import s3_select_parser


class TestIntegration(unittest.TestCase):

    def test_select_all(self):
        parsed = s3_select_parser.parseString('SELECT * FROM S3Object')
        self.assertEqual(parsed.asDict(), {
            'select': '*',
            'from': {
                'table': 'S3Object',
                'alias': None,
            }
        })

    def test_select_asterisk(self):
        parsed = s3_select_parser.parseString('SELECT * FROM S3Object[*]')
        self.assertEqual(parsed.asDict(), {
            'select': '*',
            'from': {
                'table': 'S3Object[*]',
                'alias': None,
            }
        })

    def test_table_alias_no_as(self):
        parsed = s3_select_parser.parseString('SELECT * FROM S3Object[*] my_alias')
        self.assertEqual(parsed.asDict(), {
            'select': '*',
            'from': {
                'table': 'S3Object[*]',
                'alias': 'my_alias'
            }
        })

    def test_table_alias_with_as(self):
        parsed = s3_select_parser.parseString('SELECT * FROM S3Object[*] AS my_alias')
        self.assertEqual(parsed.asDict(), {
            'select': '*',
            'from': {
                'table': 'S3Object[*]',
                'alias': 'my_alias'
            }
        })

    def test_select_with_alias(self):
        parsed = s3_select_parser.parseString(
            '''
                SELECT
                    a as my_alias_a,
                    b my_alias_b,
                    c,
                    "AS",
                    "AS" as "FrOM",
                    my_func(a, another_func(b,c)),
                    'hello ''billy'' '
                FROM
                    S3Object[*]
            ''')
        self.assertEqual(parsed.asDict(), {
            'select': [
                {'projection': 'a', 'alias': 'my_alias_a'},
                {'projection': 'b', 'alias': 'my_alias_b'},
                {'projection': 'c', 'alias': None},
                {'projection': '"AS"', 'alias': None},
                {'projection': '"AS"', 'alias': '"FrOM"'},
                {'projection': ['my_func', 'a', ['another_func', 'b', 'c']], 'alias': None},
                {'projection': "hello 'billy' ", 'alias': None},
            ],
            'from': {
                'table': 'S3Object[*]',
                'alias': None,
            }
        })
