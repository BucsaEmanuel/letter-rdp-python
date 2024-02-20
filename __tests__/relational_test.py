tests = [
    (
        """
        x > 0;
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "BinaryExpression",
                        "operator": ">",
                        "left": {
                            "type": "Identifier",
                            "value": "x",
                        },
                        "right": {
                            "type": "NumericLiteral",
                            "value": 0,
                        }
                    }
                }
            ]
        }
    ),
]
