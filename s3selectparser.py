from pyparsing import (
    CaselessKeyword,
    Keyword,
    Word,
    alphas,
    alphanums,
    delimitedList,
)

SELECT, FROM = map(
    CaselessKeyword, 'select from'.split()
)
ASTERISK = Keyword('*')

identifier = Word(alphas, alphanums + '_').setName('identifier')
projections = (delimitedList(identifier) | ASTERISK).setResultsName('projections')

s3_select_parser = \
    SELECT + \
    projections + \
    FROM + \
    'S3Object'
