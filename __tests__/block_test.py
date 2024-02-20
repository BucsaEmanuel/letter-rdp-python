tests = [
    (
        """
            {
                42;
                
                "hello";
            }
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "BlockStatement",
                    "body": [
                        {
                            "type": "ExpressionStatement",
                            "expression": {
                                "type": "NumericLiteral",
                                "value": 42
                            }
                        },
                        {
                            "type": "ExpressionStatement",
                            "expression": {
                                "type": "StringLiteral",
                                "value": "hello"
                            }
                        }
                    ]
                }
            ]
        }
    ),
    (
        """
            {
                
            }
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "BlockStatement",
                    "body": []
                }
            ]
        }
    ),
    (
        """
            {
                42;
                {
                    "hello";
                }
            }
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "BlockStatement",
                    "body": [
                        {
                            "type": "ExpressionStatement",
                            "expression": {
                                "type": "NumericLiteral",
                                "value": 42
                            }
                        },
                        {
                            "type": "BlockStatement",
                            "body": [
                                {
                                    "type": "ExpressionStatement",
                                    "expression": {
                                        "type": "StringLiteral",
                                        "value": "hello"
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ),
]