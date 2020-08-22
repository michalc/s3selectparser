# Parses S3 Select as described at
# https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-glacier-select-sql-reference.html
#
# Only the S3 form is supported

from pyparsing import (
    CaselessKeyword,
    Group,
    Keyword,
    Optional,
    Word,
    Suppress,
    alphas,
    alphanums,
    delimitedList,
)

SELECT, FROM, AS = map(
    CaselessKeyword, 'select from as'.split()
)
ASTERISK = Keyword('*')('*')
identifier = Word(alphas, alphanums + '_').setName('identifier')


#############
# SELECT List
#
# SELECT *
# SELECT projection [ AS column_alias | column_alias ] [, ...]

def projection_transform(_, __, tokens):
    d = tokens.asDict()
    return {
        **d,
        **({
            'column_alias': d['projection']
        } if 'column_alias' not in d else {})
    }


projection = \
    (identifier('projection') + Optional(Suppress(AS) + identifier('column_alias'))) \
    .setParseAction(projection_transform)
select_list = (delimitedList(projection) | ASTERISK)('select_list')


#############
# FROM Clause
#
# Table form:
# FROM S3Object
# FROM S3Object alias
# FROM S3Object AS alias
#
# JSON form:
# FROM S3Object[*].path
# FROM S3Object[*].path alias
# FROM S3Object[*].path AS alias

from_clause = Group(identifier + Optional(Suppress('[*]')))('table_name')

s3_select_parser = \
    SELECT + \
    select_list + \
    FROM + \
    from_clause
