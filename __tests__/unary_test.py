tests = [
    (
        """
        -x;
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "UnaryExpression",
                        "operator": "-",
                        "argument": {
                            "type": "Identifier",
                            "name": "x",
                        }
                    }
                }
            ]
        }
    ),
    (
        """
        !x;
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "UnaryExpression",
                        "operator": "!",
                        "argument": {
                            "type": "Identifier",
                            "name": "x",
                        }
                    }
                }
            ]
        }
    ),
]
