tests = [
    # NumericLiteral
    ('42;', {
        "type": "Program",
        "body": [
            {
                "type": "ExpressionStatement",
                "expression": {
                    "type": "NumericLiteral",
                    "value": 42
                }
            }
        ]
    }),

    # StringLiteral
    ('"hello";', {
        "type": "Program",
        "body": [
            {
                "type": "ExpressionStatement",
                "expression": {
                    "type": "StringLiteral",
                    "value": "hello"
                }
            }
        ]
    }),

    # StringLiteral
    ("'hello';", {
        "type": "Program",
        "body": [
            {
                "type": "ExpressionStatement",
                "expression": {
                    "type": "StringLiteral",
                    "value": "hello"
                }
            }
        ]
    }),
]