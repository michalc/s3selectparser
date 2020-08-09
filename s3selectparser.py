from pyparsing import (
    CaselessKeyword,
)

SELECT, FROM = map(
    CaselessKeyword, 'select from'.split()
)

s3_select_parser = \
    SELECT + \
    '*' + \
    FROM + \
    'S3Object'
