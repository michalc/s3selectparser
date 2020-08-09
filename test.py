import unittest

from s3selectparser import s3_select_parser


class TestIntegration(unittest.TestCase):

    def test_parser(self):
        parsed = s3_select_parser.parseString('SELECT * FROM S3Object')
        self.assertEqual(list(parsed), ['select', '*', 'from', 'S3Object'])
