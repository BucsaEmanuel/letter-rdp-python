tests = [
    # Addition
    (
        """
            2 + 2;
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "BinaryExpression",
                        "operator": {
                            "type": "ADDITIVE_OPERATOR",
                            "value": "+",
                        },
                        "left": {
                            "type": "NumericLiteral",
                            "value": 2
                        },
                        "right": {
                            "type": "NumericLiteral",
                            "value": 2
                        }
                    }
                }
            ]
        }
    ),
    # Nested binary expressions
    # left: 3 + 2
    # right: 2
    (
        """
            3 + 2 - 2;
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "BinaryExpression",
                        "operator": {
                            "type": "ADDITIVE_OPERATOR",
                            "value": "-",
                        },
                        "left": {
                            "type": "BinaryExpression",
                            "operator": {
                                "type": "ADDITIVE_OPERATOR",
                                "value": "+",
                            },
                            "left": {
                                "type": "NumericLiteral",
                                "value": 3
                            },
                            "right": {
                                "type": "NumericLiteral",
                                "value": 2
                            }
                        },
                        "right": {
                            "type": "NumericLiteral",
                            "value": 2
                        }
                    }
                }
            ]
        }
    ),
    (
        """
            2 * 2;
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "BinaryExpression",
                        "operator": {
                            "type": "MULTIPLICATIVE_OPERATOR",
                            "value": "*",
                        },
                        "left": {
                          "type": "NumericLiteral",
                          "value": 2,
                        },
                        "right": {
                          "type": "NumericLiteral",
                          "value": 2,
                        },
                    }
                }
            ]
        }
    ),
    # Precedence of operations:
    (
        """
            2 + 2 * 2;
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "BinaryExpression",
                        "operator": {
                            "type": "ADDITIVE_OPERATOR",
                            "value": "+",
                        },
                        "left": {
                          "type": "NumericLiteral",
                          "value": 2,
                        },
                        "right": {
                            "type": "BinaryExpression",
                            "operator": {
                                "type": "MULTIPLICATIVE_OPERATOR",
                                "value": "*",
                            },
                            "left": {
                                "type": "NumericLiteral",
                                "value": 2
                            },
                            "right": {
                                "type": "NumericLiteral",
                                "value": 2
                            }
                        }
                    }
                }
            ]
        }
    ),
    # Precedence of operations:
    (
        """
            (2 + 2) * 2;
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "BinaryExpression",
                        "operator": {
                            "type": "MULTIPLICATIVE_OPERATOR",
                            "value": "*",
                        },
                        "left": {
                            "type": "BinaryExpression",
                            "operator": {
                                "type": "ADDITIVE_OPERATOR",
                                "value": "+",
                            },
                            "left": {
                                "type": "NumericLiteral",
                                "value": 2
                            },
                            "right": {
                                "type": "NumericLiteral",
                                "value": 2
                            }
                        },
                        "right": {
                            "type": "NumericLiteral",
                            "value": 2,
                        },
                    }
                }
            ]
        }
    ),
]