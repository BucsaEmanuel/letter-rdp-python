tests = [
    # Simple variable declaration:
    (
        """
        let x = 42;
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "VariableStatement",
                    "declarations": [
                        {
                            "type": "VariableDeclaration",
                            "id": {
                                "type": "Identifier",
                                "name": "x",
                            },
                            "init": {
                                "type": "NumericLiteral",
                                "value": 42,
                            }
                        }
                    ]
                }
            ]
        }
    ),
    # Variable declaration, no init:
    (
        """
        let x;
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "VariableStatement",
                    "declarations": [
                        {
                            "type": "VariableDeclaration",
                            "id": {
                                "type": "Identifier",
                                "name": "x",
                            },
                            "init": None
                        }
                    ]
                }
            ]
        }
    ),
    # Multiple variable declarations, no init:
    (
        """
        let x, y;
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "VariableStatement",
                    "declarations": [
                        {
                            "type": "VariableDeclaration",
                            "id": {
                                "type": "Identifier",
                                "name": "x",
                            },
                            "init": None
                        },
                        {
                            "type": "VariableDeclaration",
                            "id": {
                                "type": "Identifier",
                                "name": "y",
                            },
                            "init": None
                        },
                    ]
                }
            ]
        }
    ),
    # Multiple variable declarations:
    (
        """
        let x, y = 42;
        """,
        {
            "type": "Program",
            "body": [
                {
                    "type": "VariableStatement",
                    "declarations": [
                        {
                            "type": "VariableDeclaration",
                            "id": {
                                "type": "Identifier",
                                "name": "x",
                            },
                            "init": None
                        },
                        {
                            "type": "VariableDeclaration",
                            "id": {
                                "type": "Identifier",
                                "name": "y",
                            },
                            "init": {
                                "type": "NumericLiteral",
                                "value": 42,
                            }
                        },
                    ]
                }
            ]
        }
    ),

]