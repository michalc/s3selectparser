from pyparsing import (
    CaselessKeyword,
    Group,
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

identifier_all_rows = Group(identifier + '[*]')
table_name = (identifier_all_rows | identifier).setResultsName('table_name')

s3_select_parser = \
    SELECT + \
    projections + \
    FROM + \
    table_name
