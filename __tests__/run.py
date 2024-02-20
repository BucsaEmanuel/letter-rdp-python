import json
from __tests__.literals_test import tests as literals_tests
from __tests__.statement_list_test import tests as statement_list_tests
from __tests__.block_test import tests as block_tests
from __tests__.empty_statement_test import tests as empty_statement_tests
from __tests__.math_test import tests as math_tests
from __tests__.assignment_test import tests as assignment_tests
from __tests__.variable_test import tests as variable_tests
from __tests__.if_test import tests as if_tests
from __tests__.relational_test import tests as relational_tests
from __tests__.equality_test import tests as equality_tests
from __tests__.logical_test import tests as logical_tests
from __tests__.unary_test import tests as unary_tests
from __tests__.while_test import tests as while_tests
from __tests__.do_while_test import tests as do_while_tests
from __tests__.for_test import tests as for_tests
from __tests__.function_declaration_test import tests as function_declaration_tests
from __tests__.member_test import tests as member_tests
from __tests__.call_test import tests as call_tests
from __tests__.class_test import tests as class_tests
from deepdiff import DeepDiff
from src.Parser import Parser

parser = Parser()


# For manual tests
def execute():
    program = """
    
    class Point {
        def constructor(x, y) {
            this.x = x;
            this.y = y;
        }
        
        def calc() {
            return this.x + this.y;
        }
    }
    
    class Point3D extends Point {
        def constructor(x, y, z) {
            super(x, y);
            this.z = z;
        }
        
        def calc() {
            return super() + this.z;
        }
    }
    
    let p = new Point3D(10, 20, 30);
    
    p.calc();
        
    """

    ast = parser.parse(program)

    print(json.dumps(ast, indent=4))


# Manual test
execute()

"""
Test function
"""


def test(program, expected):
    ast = parser.parse(program)
    difference = DeepDiff(ast, expected)
    try:
        assert difference.get('values_changed') is None
    except AssertionError:
        raise AssertionError(f"\nExpected:\n{json.dumps(expected, indent=4)}\nbut got:\n{json.dumps(ast, indent=4)}")


tests = literals_tests + statement_list_tests + block_tests + empty_statement_tests + math_tests + assignment_tests + \
         variable_tests + if_tests + relational_tests + equality_tests + logical_tests + unary_tests + while_tests + \
         do_while_tests + for_tests + function_declaration_tests + member_tests + call_tests + class_tests
for testcase in tests:
    test(testcase[0], testcase[1])

print(f"All assertions passed!")
