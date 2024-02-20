tests = [
    (
        """
        foo(x);
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "CallExpression",
                        "callee": {
                            "type": "Identifier",
                            "name": "foo",
                        },
                        "arguments": [
                            {
                                "type": "Identifier",
                                "name": "x",
                            },
                        ],
                    },
                },
            ],
        },
    ),
    (
        """
        foo(x)();
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "CallExpression",
                        "callee": {
                            "type": "CallExpression",
                            "callee": {
                                "type": "Identifier",
                                "name": "foo",
                            },
                            "arguments": [
                                {
                                    "type": "Identifier",
                                    "name": "x",
                                },
                            ],
                        },
                        "arguments": [],
                    },
                },
            ],
        },
    ),
    (
        """
        console.log(x, y);
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "ExpressionStatement",
                    "expression": {
                        "type": "CallExpression",
                        "callee": {
                            "type": "MemberExpression",
                            "computed": False,
                            "object": {
                                "type": "Identifier",
                                "name": "console",
                            },
                            "property": {
                                "type": "Identifier",
                                "name": "log",
                            },
                        },
                        "arguments": [
                            {
                                "type": "Identifier",
                                "name": "x",
                            },
                            {
                                "type": "Identifier",
                                "name": "y",
                            },
                        ],
                    },
                },
            ],
        },
    ),
]
