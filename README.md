# s3selectparser

Experimental S3 Select parser


## Installation

```bash
pip install s3selectparser
```


## Usage

The underlying pyparsing parser is exposed as `s3_select_parser`.

```python
from s3selectparser import s3_select_parser

parsed = s3_select_parser.parseString(
    '''
        SELECT
            a as my_alias_a,
            b my_alias_b,
            c,
            "AS",
            "AS" as "FrOM",
            my_func(a, another_func(47, c)),
            'hello ''billy'' '
        FROM
            S3Object[*]
    ''')
print(parsed.asDict())
```
