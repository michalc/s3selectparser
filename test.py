import unittest

from s3selectparser import s3_select_parser


class TestIntegration(unittest.TestCase):

    def test_select_all(self):
        parsed = s3_select_parser.parseString('SELECT * FROM S3Object')
        self.assertEqual(parsed.asDict(), {
            'projections': ['*']
        })

    def test_select_columns(self):
        parsed = s3_select_parser.parseString('SELECT a, b, c FROM S3Object')
        self.assertEqual(parsed.asDict(), {
            'projections': ['a', 'b', 'c']
        })
