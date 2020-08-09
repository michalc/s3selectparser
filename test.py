import unittest

from s3selectparser import parse_s3_select


class TestIntegration(unittest.TestCase):

    def test_parser(self):
        parse_s3_select()
