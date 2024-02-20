from .Tokenizer import Tokenizer
from src.common.Number import Number


class Parser:
    def __init__(self):
        # self._lookahead = None
        # self._string = ''
        self._tokenizer = Tokenizer()

    def parse(self, string):
        """
        Parses a string into an AST.
        :param string:
        """
        self._string = string
        self._tokenizer.init(string)

        """
        Prime the tokenizer to obtain the first
        token which is our lookahead. The lookahead is
        used for predictive parsing.
        """
        self._lookahead = self._tokenizer.getNextToken()
        """
        Parse recursively starting from the main
        entry point, the Program:
        """
        return self.Program()

    def Program(self):
        """
        Main entry point.

        Program
        : StatementList
        ;
        """
        return {
            "type": "Program",
            "body": self.StatementList(),
        }

    def StatementList(self, stopLookAhead=None):
        """
        StatementList
            : Statement
            | StatementList Statement -> Statement Statement Statement Statement
            ;
        """
        statementList = [self.Statement()]

        while self._lookahead is not None and self._lookahead['type'] != stopLookAhead:
            statementList.append(self.Statement())

        return statementList

    def Statement(self):
        """
        Statement
            : ExpressionStatement
            | BlockStatement
            | EmptyStatement
            | VariableStatement
            | IfStatement
            | IterationStatement
            | FunctionDeclaration
            | ReturnStatement
            | ClassDeclaration
            ;
        """
        match self._lookahead['type']:
            case ';':
                return self.EmptyStatement()
            case 'if':
                return self.IfStatement()
            case '{':
                return self.BlockStatement()
            case 'let':
                return self.VariableStatement()
            case 'def':
                return self.FunctionDeclaration()
            case 'class':
                return self.ClassDeclaration()
            case 'return':
                return self.ReturnStatement()
            case 'while' | 'do' | 'for':
                return self.IterationStatement()
            case _:
                return self.ExpressionStatement()

    def ClassDeclaration(self):
        """
        ClassDeclaration
            : 'class' Identifier OptClassExtends BlockStatement
            ;
        """
        self._eat('class')
        identifier = self.Identifier()
        superClass = self.ClassExtends() if self._lookahead['type'] == 'extends' else None
        body = self.BlockStatement()

        return {
            "type": "ClassDeclaration",
            "id": identifier,
            "superClass": superClass,
            "body": body
        }

    def ClassExtends(self):
        """
        ClassExtends
            : 'extends' Identifier
            ;
        """
        self._eat('extends')
        return self.Identifier()

    def FunctionDeclaration(self):
        """
        FunctionDeclaration
            : 'def' Identifier '(' OptFormalParameterList ')' BlockStatement
            ;
        """
        self._eat('def')
        name = self.Identifier()
        self._eat('(')

        # OptFormalParameterList
        params = self.FormalParameterList() if self._lookahead['type'] != ')' else []

        self._eat(')')

        body = self.BlockStatement()

        return {
            "type": 'FunctionDeclaration',
            "name": name,
            "params": params,
            "body": body
        }

    def FormalParameterList(self):
        """
        FormalParameterList
             : Identifier
             | FormalParameterList ',' Identifier
             ;
        """
        params = [self.Identifier()]
        while self._lookahead['type'] == ',' and self._eat(','):
            params.append(self.Identifier())

        return params

    def ReturnStatement(self):
        """
        ReturnStatement
            : 'return' OptExpression ';'
            ;
        """
        self._eat('return')
        argument = self.Expression() if self._lookahead['type'] != ';' else None
        self._eat(';')
        return {
            "type": 'ReturnStatement',
            "argument": argument,
        }


    def IterationStatement(self):
        """
        IterationStatement
            : WhileStatement
            | DoWhileStatement
            | ForStatement
            ;
        """
        match self._lookahead['type']:
            case 'while':
                return self.WhileStatement()
            case 'do':
                return self.DoWhileStatement()
            case 'for':
                return self.ForStatement()

    def WhileStatement(self):
        """
        WhileStatement
            : 'while' '(' Expression ')' Statement
            ;
        """
        self._eat('while')

        self._eat('(')
        test = self.Expression()
        self._eat(')')

        body = self.Statement()

        return {
            "type": "WhileStatement",
            "test": test,
            "body": body,
        }

    def DoWhileStatement(self):
        """
        DoWhileStatement
            : 'do' Statement 'while' '(' Expression ')' ';'
        """
        self._eat('do')

        body = self.Statement()

        self._eat('while')
        self._eat('(')
        test = self.Expression()
        self._eat(')')

        self._eat(';')

        return {
            "type": "DoWhileStatement",
            "body": body,
            "test": test,
        }

    def ForStatement(self):
        """
        ForStatement
            : 'for' '(' OptForStatementInit ';' OptExpression ';' OptExpression ')' Statement
            ;
        """
        self._eat('for')
        self._eat('(')

        init = self.ForStatementInit() if self._lookahead['type'] != ';' else None
        self._eat(';')

        test = self.Expression() if self._lookahead['type'] != ';' else None
        self._eat(';')

        update = self.Expression() if self._lookahead['type'] != ')' else None
        self._eat(')')

        body = self.Statement()

        return {
            "type": "ForStatement",
            "init": init,
            "test": test,
            "update": update,
            "body": body
        }

    def ForStatementInit(self):
        """
        ForStatementInit
            : VariableStatementInit
            | Expression
            ;
        """
        if self._lookahead['type'] == 'let':
            return self.VariableStatementInit()
        return self.Expression()

    def IfStatement(self):
        """
        IfStatement
            : 'if' '(' Expression ')' Statement
            | 'if' '(' Expression ')' Statement 'else' Statement
            ;
        """
        self._eat('if')
        self._eat('(')
        test = self.Expression()
        self._eat(')')
        consequent = self.Statement()
        alternate = self._eat("else") and self.Statement() if self._lookahead is not None and self._lookahead[
            'type'] == 'else' else None

        return {
            "type": "IfStatement",
            "test": test,
            "consequent": consequent,
            "alternate": alternate
        }

    def VariableStatementInit(self):
        """
        VariableStatementInit
            : 'let' VariableDeclarationList
            ;
        """
        self._eat('let')
        declarations = self.VariableDeclarationList()
        return {
            "type": "VariableStatement",
            "declarations": declarations,
        }

    def VariableStatement(self):
        """
        VariableStatement
            : 'let' VariableDeclarationList ';'
            ;
        """
        variableStatement = self.VariableStatementInit()
        self._eat(';')
        return variableStatement

    def VariableDeclarationList(self):
        """
        VariableDeclarationList
            : VariableDeclaration
            | VariableDeclarationList ',' VariableDeclaration
            ;
        """
        declarations = []
        while True:
            declarations.append(self.VariableDeclaration())
            if not (self._lookahead['type'] == ',' and self._eat(',')):
                break
        return declarations

    def VariableDeclaration(self):
        """
        VariableDeclaration
            : Identifier OptVariableInitializer
            ;
        """
        identifier = self.Identifier()

        # OptVariableInitializer
        init = self.VariableInitializer() if self._lookahead['type'] != ";" and self._lookahead['type'] != "," else None

        return {
            "type": "VariableDeclaration",
            "id": identifier,
            "init": init,
        }

    def VariableInitializer(self):
        """
        VariableInitializer
            : SIMPLE_ASSIGN AssignmentExpression
            ;
        """
        self._eat("SIMPLE_ASSIGN")
        return self.AssignmentExpression()

    def EmptyStatement(self):
        """
        EmptyStatement
            : ';'
            ;
        """
        self._eat(';')
        return {
            "type": "EmptyStatement"
        }

    def BlockStatement(self):
        """
        BlockStatement
            : '{' OptStatementList '}'
            ;
        """
        self._eat('{')

        body = self.StatementList('}') if self._lookahead['type'] != '}' else []

        self._eat('}')

        return {
            "type": "BlockStatement",
            "body": body
        }

    def ExpressionStatement(self):
        """
        ExpressionStatement
            : Expression ';'
            ;
        """
        expression = self.Expression()
        self._eat(';')
        return {
            "type": "ExpressionStatement",
            "expression": expression
        }

    def Expression(self):
        """
        Expression
            : Literal
            ;
        """
        return self.AssignmentExpression()

    def AssignmentExpression(self):
        """
        AssignmentExpression
            : LogicalORExpression
            | LeftHandSideExpression AssignmentOperator AssignmentExpression
            ;
        """
        left = self.LogicalORExpression()
        if not self._isAssignmentOperator(self._lookahead['type']):
            return left

        return {
            "type": "AssignmentExpression",
            "operator": self.AssignmentOperator()["value"],
            "left": self._checkValidAssignmentTarget(left),
            "right": self.AssignmentExpression(),
        }

    def RelationalExpression(self):
        """
        RELATIONAL_OPERATOR: >, >=, <, <=

          x > y
          x >= y
          x < y
          x <= y

        RelationalExpression
            : AdditiveExpression
            | AdditiveExpression RELATIONAL_OPERATOR RelationalExpression
            ;
        """
        return self._BinaryExpression(
            "AdditiveExpression",
            "RELATIONAL_OPERATOR",
        )

    def Identifier(self):
        """
        Identifier
            : IDENTIFIER
            ;
        """
        name = self._eat("IDENTIFIER")['value']
        return {
            "type": "Identifier",
            "name": name,
        }

    def _checkValidAssignmentTarget(self, node):
        """
        Extra check whether it's valid assignment target
        """
        if node['type'] in ['Identifier', 'MemberExpression']:
            return node
        raise SyntaxError(f"Invalid left-hand side in assignment expression")

    def _isAssignmentOperator(self, tokenType):
        return tokenType in ("SIMPLE_ASSIGN", "COMPLEX_ASSIGN")

    def AssignmentOperator(self):
        """
        AssignmentOperator
            : SIMPLE_ASSIGN
            | COMPLEX_ASSIGN
            ;
        """
        if self._lookahead['type'] == 'SIMPLE_ASSIGN':
            return self._eat('SIMPLE_ASSIGN')
        return self._eat('COMPLEX_ASSIGN')

    def LogicalANDExpression(self):
        """
        Logical AND expression

            x && y

        LogicalANDExpression
            : EqualityExpression LOGICAL_AND LogicalANDExpression
            | EqualityExpression
            ;
        """
        return self._LogicalExpression('EqualityExpression', 'LOGICAL_AND')

    def LogicalORExpression(self):
        """
        Logical OR expression

            x || y

        LogicalORExpression
            : LogicalANDExpression LOGICAL_OR LogicalORExpression
            | LogicalORExpression
            ;
        """
        return self._LogicalExpression('LogicalANDExpression', 'LOGICAL_OR')

    def EqualityExpression(self):
        """
        EQUALITY_OPERATOR: ==, !=

            x == y
            x != y
        EqualityExpression
            : RelationalExpression EQUALITY_OPERATOR EqualityExpression
            | RelationalExpression
            ;
        """
        return self._BinaryExpression('RelationalExpression', 'EQUALITY_OPERATOR')

    def AdditiveExpression(self):
        """
        AdditiveExpression
            : MultiplicativeExpression
            | AdditiveExpression ADDITIVE_OPERATOR MultiplicativeExpression -> MultiplicativeExpression ADDITIVE_OPERATOR
            ;
        """
        return self._BinaryExpression('MultiplicativeExpression', 'ADDITIVE_OPERATOR')

    def _BinaryExpression(self, builderName, operatorToken):
        """
        Generic binary expression
        """
        left = getattr(self, builderName)()

        while self._lookahead['type'] == operatorToken:
            operator = self._eat(operatorToken)['value']
            right = getattr(self, builderName)()

            left = {
                "type": "BinaryExpression",
                "operator": operator,
                "left": left,
                "right": right
            }

        return left

    def MultiplicativeExpression(self):
        """
        AdditiveExpression
            : UnaryExpression
            | MultiplicativeExpression MULTIPLICATIVE_OPERATOR UnaryExpression
            ;
        """
        return self._BinaryExpression('UnaryExpression', 'MULTIPLICATIVE_OPERATOR')

    def _LogicalExpression(self, builderName, operatorToken):
        """
        Generic helper for LogicalExpression nodes.
        """
        left = getattr(self, builderName)()

        while self._lookahead['type'] == operatorToken:
            operator = self._eat(operatorToken)['value']
            right = getattr(self, builderName)()

            left = {
                "type": "LogicalExpression",
                "operator": operator,
                "left": left,
                "right": right
            }

        return left

    def UnaryExpression(self):
        """
        UnaryExpression
            : LeftHandSideExpression
            | ADDITIVE_OPERATOR UnaryExpression
            | LOGICAL_NOT UnaryExpression
            ;
        """
        operator = None
        match self._lookahead['type']:
            case 'ADDITIVE_OPERATOR':
                operator = self._eat('ADDITIVE_OPERATOR')['value']
            case 'LOGICAL_NOT':
                operator = self._eat('LOGICAL_NOT')['value']

        if operator is not None:
            return {
                "type": "UnaryExpression",
                "operator": operator,
                "argument": self.UnaryExpression(),
            }
        return self.LeftHandSideExpression()

    def LeftHandSideExpression(self):
        """
        LeftHandSideExpression
            : CallMemberExpression
        """
        return self.CallMemberExpression()

    def CallMemberExpression(self):
        """
        CallMemberExpression
            : MemberExpression
            | CallExpression
            ;
        """
        if self._lookahead['type'] == 'super':
            return self._CallExpression(self.Super())

        # Member part, might be part of a call:
        member = self.MemberExpression()

        # See if we have a call expression:
        if self._lookahead['type'] == '(':
            return self._CallExpression(member)

        # Simple member expression
        return member

    def _CallExpression(self, callee):
        """
        Generic call expression helper.

        CallExpression
            : Callee Arguments
            ;

        Callee
            : MemberExpression
            | CallExpression
            ;
        """
        callExpression = {
            "type": "CallExpression",
            "callee": callee,
            "arguments": self.Arguments(),
        }

        if self._lookahead['type'] == '(':
            callExpression = self._CallExpression(callExpression)

        return callExpression

    def Arguments(self):
        """
        Arguments
            : '(' OptArgumentList ')'
            ;
        """
        self._eat('(')
        argumentList = self.ArgumentList() if self._lookahead['type'] != ')' else []
        self._eat(')')

        return argumentList

    def ArgumentList(self):
        """
        ArgumentList
            : AssignmentExpression
            | ArgumentList ',' AssignmentExpression
            ;
        """
        argumentList = [self.AssignmentExpression()]

        while self._lookahead['type'] == ',' and self._eat(','):
            argumentList.append(self.AssignmentExpression())

        return argumentList

    def MemberExpression(self):
        """
        MemberExpression
            : PrimaryExpression
            | MemberExpression '.' Identifier
            | MemberExpression '[' Expression ']'
            ;
        """
        obj = self.PrimaryExpression()

        while self._lookahead['type'] == '.' or self._lookahead['type'] == '[':
            # MemberExpression '.' Identifier
            if self._lookahead['type'] == '.':
                self._eat('.')
                prop = self.Identifier()
                obj = {
                    "type": "MemberExpression",
                    "computed": False,
                    "object": obj,
                    "property": prop,
                }
            # MemberExpression '[' Expression ']'
            if self._lookahead['type'] == '[':
                self._eat('[')
                prop = self.Expression()
                self._eat(']')
                obj = {
                    "type": "MemberExpression",
                    "computed": True,
                    "object": obj,
                    "property": prop
                }
        return obj

    def PrimaryExpression(self):
        """
        PrimaryExpression
            : Literal
            | ParenthesizedExpression
            | Identifier
            | ThisExpression
            | NewExpression
            ;
        """
        if self._isLiteral(self._lookahead['type']):
            return self.Literal()
        match self._lookahead['type']:
            case '(':
                return self.ParenthesizedExpression()
            case "IDENTIFIER":
                return self.Identifier()
            case "this":
                return self.ThisExpression()
            case "new":
                return self.NewExpression()
            case _:
                return self.LeftHandSideExpression()

    def NewExpression(self):
        """
        NewExpression
            : 'new' MemberExpression Arguments
        """
        self._eat('new')
        return {
            "type": "NewExpression",
            "callee": self.MemberExpression(),
            "arguments": self.Arguments(),
        }

    def ThisExpression(self):
        """
        ThisExpression
            : 'this'
            ;
        """
        self._eat('this')
        return {
            "type": "ThisExpression",
        }

    def Super(self):
        """
        Super
            : 'super'
            ;
        """
        self._eat('super')
        return {
            "type": "Super",
        }

    def _isLiteral(self, tokenType):
        """
        Whether the token is a literal.
        """
        return tokenType in ("NUMBER", "STRING", "true", "false", "null")

    def ParenthesizedExpression(self):
        """
        ParenthesizedExpression
            : '(' Expression ')'
            ;
        """
        self._eat('(')
        expression = self.Expression()
        self._eat(')')
        return expression

    def Literal(self):
        """
        Literal
            : NumericLiteral
            | StringLiteral
            | BooleanLiteral
            | NullLiteral
            ;
        """
        match self._lookahead['type']:
            case 'NUMBER':
                return self.NumericLiteral()
            case 'STRING':
                return self.StringLiteral()
            case 'true':
                return self.BooleanLiteral(True)
            case 'false':
                return self.BooleanLiteral(False)
            case 'null':
                return self.NullLiteral()
        raise SyntaxError(f"Literal: unexpected literal production")

    def BooleanLiteral(self, value):
        """
        BooleanLiteral
            : 'true'
            | 'false'
            ;
        """
        self._eat('true' if value else 'false')
        return {
            "type": "BooleanLiteral",
            "value": value
        }

    def NullLiteral(self):
        """
        NullLiteral
            : 'null'
            ;
        """
        self._eat('null')
        return {
            "type": "NullLiteral",
            "value": None
        }

    def StringLiteral(self):
        """
        StringLiteral
        : STRING
        ;
        """
        token = self._eat('STRING')
        return {
            "type": "StringLiteral",
            "value": token['value'][1:-1]
        }

    def NumericLiteral(self):
        token = self._eat('NUMBER')
        """
        NumericLiteral
        : NUMBER
        ;
        """
        return {
            "type": 'NumericLiteral',
            "value": Number(token["value"])
        }

    def _eat(self, tokenType):
        """
        Expects a token of a given type
        :param tokenType:
        """
        token = self._lookahead

        if token is None:
            raise SyntaxError(f"Unexpected end of input, expected {tokenType}")

        if token['type'] != tokenType:
            raise SyntaxError(f"Unexpected token: \"{token['value']}\", expected: \"{tokenType}\"")

        # Advance to next token.
        self._lookahead = self._tokenizer.getNextToken()

        return token
