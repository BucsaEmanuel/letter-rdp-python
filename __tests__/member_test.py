tests = [
    (
        """
        x.y;
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "MemberExpression",
                        "computed": False,
                        "object": {
                            "type": "Identifier",
                            "name": "x",
                        },
                        "property": {
                            "type": "Identifier",
                            "name": "y",
                        },
                    },
                },
            ],
        }
    ),
    (
        """
        x.y = 1;
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "AssignmentExpression",
                        "operator": "=",
                        "left": {
                            "type": "MemberExpression",
                            "computed": False,
                            "object": {
                                "type": "Identifier",
                                "name": "x",
                            },
                            "property": {
                                "type": "Identifier",
                                "name": "y",
                            }
                        },
                        "right": {
                            "type": "NumericLiteral",
                            "value": 1,
                        },
                    },
                },
            ],
        },
    ),
    (
        """
        x[0] = 1;
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "AssignmentExpression",
                        "operator": "=",
                        "left": {
                            "type": "MemberExpression",
                            "computed": True,
                            "object": {
                                "type": "Identifier",
                                "name": "x",
                            },
                            "property": {
                                "type": "NumericLiteral",
                                "name": 0,
                            }
                        },
                        "right": {
                            "type": "NumericLiteral",
                            "value": 1,
                        },
                    },
                },
            ],
        },
    ),
    (
        """
        a.b.c['d'];
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "MemberExpression",
                        "computed": True,
                        "object": {
                            "type": "MemberExpression",
                            "computed": False,
                            "object": {
                                "type": "MemberExpression",
                                "computed": False,
                                "object": {
                                    "type": "Identifier",
                                    "name": "a",
                                },
                                "property": {
                                    "type": "Identifier",
                                    "name": "b"
                                }
                            },
                            "property": {
                                "type": "Identifier",
                                "name": "c",
                            }
                        },
                        "property": {
                            "type": "StringLiteral",
                            "name": "d",
                        },
                    },
                },
            ],
        },
    ),
]
