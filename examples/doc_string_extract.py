"""
Extract the doc-string at the beginning of a file.

Pieced together from 
  http://www.python.org/doc/lib/node774.html
"Python Library Reference", "18.1.6.2 Information Discovery"
"""


import symbol
import token
import parser

from types import ListType, TupleType

def match(pattern, data, vars=None):
    if vars is None:
        vars = {}
    if type(pattern) is ListType:
        vars[pattern[0]] = data
        return 1, vars
    if type(pattern) is not TupleType:
        return (pattern == data), vars
    if len(data) != len(pattern):
        return 0, vars
    for pattern, data in map(None, pattern, data):
        same, vars = match(pattern, data, vars)
        if not same:
            break
    return same, vars

DOCSTRING_STMT_PATTERN = (
    symbol.stmt,
    (symbol.simple_stmt,
     (symbol.small_stmt,
      (symbol.expr_stmt,
       (symbol.testlist,
        (symbol.test,
         (symbol.and_test,
          (symbol.not_test,
           (symbol.comparison,
            (symbol.expr,
             (symbol.xor_expr,
              (symbol.and_expr,
               (symbol.shift_expr,
                (symbol.arith_expr,
                 (symbol.term,
                  (symbol.factor,
                   (symbol.power,
                    (symbol.atom,
                     (token.STRING, ['docstring'])
                     )))))))))))))))),
     (token.NEWLINE, '')
     ))



# Using the match() function with this pattern,
# extracting the module docstring from the parse tree
# created previously is easy:

def get_doc_string(fname="doc_string_extract.py"):
    ast = parser.suite(open(fname).read())
    tup = ast.totuple()

    found, vars = match(DOCSTRING_STMT_PATTERN, tup[1])
    #print found
    #print vars
    return vars["docstring"].replace('"""','')
    

if __name__ == "__main__":
    print get_doc_string()
