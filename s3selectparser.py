# Parses S3 Select as described at
# https://docs.aws.amazon.com/AmazonS3/latest/dev/s3-glacier-select-sql-reference.html
#
# Only the S3 form is supported

from pyparsing import (
    CaselessKeyword,
    Combine,
    Forward,
    Group,
    Keyword,
    MatchFirst,
    Optional,
    ParserElement,
    ParseResults,
    QuotedString,
    Suppress,
    Word,
    alphas,
    alphanums,
    delimitedList,
    oneOf,
    opAssoc,
    infixNotation,
    pyparsing_common,
)
ParserElement.enablePackrat()

SELECT, FROM, AS = map(
    CaselessKeyword, 'select from as'.split()
)

reserved_keywords = map(
    CaselessKeyword,
    'absolute action add all allocate alter and any are as asc assertion at authorization avg '
    'bag begin between bit bit_length blob bool boolean both by cascade cascaded case cast '
    'catalog char char_length character character_length check clob close coalesce collate '
    'collation column commit connect connection constraint constraints continue convert '
    'corresponding count create cross current current_date current_time current_timestamp '
    'current_user cursor date day deallocate dec decimal declare default deferrable deferred '
    'delete desc describe descriptor diagnostics disconnect distinct domain double drop else '
    'end end-exec escape except exception exec execute exists external extract false fetch '
    'first float for foreign found from full get global go goto grant group having hour '
    'identity immediate in indicator initially inner input insensitive insert int integer '
    'intersect interval into is isolation join key language last leading left level like limit '
    'list local lower match max min minute missing module month names national natural nchar '
    'next no not null nullif numeric octet_length of on only open option or order outer output '
    'overlaps pad partial pivot position precision prepare preserve primary prior privileges '
    'procedure public read real references relative restrict revoke right rollback rows schema '
    'scroll second section select session session_user set sexp size smallint some space sql '
    'sqlcode sqlerror sqlstate string struct substring sum symbol system_user table temporary '
    'then time timestamp timezone_hour timezone_minute to trailing transaction translate '
    'translation trim true tuple union unique unknown unpivot update upper usage user using '
    'value values varchar varying view when whenever where with work write year zone'.split()
)
identifier = Combine(
    Combine(~MatchFirst(reserved_keywords) + Word(alphas, alphanums + '_'))
    | Group('"' + Word(alphas, alphanums + '_') + '"')
)


##############
# Expresssions

# Functions (both named and infix) are parsed as lists

expression = Forward()
function = (
    Word(alphas, alphanums + '_')('name')
    + Suppress('(') + delimitedList(expression)('arguments') + Suppress(')')
).setParseAction(lambda tokens: [list(tokens)])
string_literal = QuotedString("'", escQuote="''")
numeric_literal = pyparsing_common.fnumber
pre_infix_expression = function | string_literal | numeric_literal | identifier
expression <<= infixNotation(pre_infix_expression, [
    ('-', 1, opAssoc.RIGHT),
    (oneOf('* / %'), 2, opAssoc.LEFT),
    (oneOf('+ -'), 2, opAssoc.LEFT),
    (CaselessKeyword('in'), 2, opAssoc.LEFT),
    (CaselessKeyword('between'), 2, opAssoc.LEFT),
    (CaselessKeyword('like'), 2, opAssoc.LEFT),
    (oneOf('< > <= >='), 2, opAssoc.LEFT),
    ('=', 2, opAssoc.RIGHT),
    (CaselessKeyword('not'), 1, opAssoc.RIGHT),
    (CaselessKeyword('and'), 2, opAssoc.LEFT),
    (CaselessKeyword('or'), 2, opAssoc.LEFT),
]).setParseAction(
    # If tokens[0] is a ParseResults, it's an infix expression
    lambda tokens: [list(tokens[0])] if isinstance(tokens[0], ParseResults) else tokens
)


#############
# SELECT List
#
# SELECT *
# SELECT projection [ AS column_alias | column_alias ] [, ...]

projection = \
    (expression('projection') + Optional(Optional(AS) + identifier('alias'))) \
    .setParseAction(lambda tokens: {
        'projection': tokens['projection'],
        'alias': tokens.get('alias'),
    })


select = \
    (delimitedList(projection) | Keyword('*'))('select') \
    .setParseAction(lambda tokens: '*' if list(tokens) == ['*'] else tokens)


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

table = (
    Combine(Group(Keyword('S3Object[*]') | Keyword('S3Object')))('table')
    + Optional(Optional(AS) + identifier('alias'))
)('from').setParseAction(lambda tokens: {
    'table': tokens['table'],
    'alias': tokens.get('alias')
})

s3_select_parser = \
    SELECT + \
    select + \
    FROM + \
    table
