from enum import Enum
from lexer import TAG, Token
from error import SyntaxError
from gen import Lvalue, Rvalue
import globals


# Definimos uma exceção personalizada para evitar confusão
# com o "SemanticErrorAST" nativo do Python
class SemanticErrorAST(Exception):
    def __init__(self, message="Erro semântico"):
        self.message = message
        super().__init__(self.message)


class ExprType(Enum):
    VOID = 0
    INT = 1
    FLOAT = 2
    BOOL = 3

class NodeType(Enum):
    UNKNOWN = 0
    STMT = 1
    EXPR = 2
    CONSTANT = 3
    IDENTIFIER = 4
    ACCESS = 5
    LOG = 6
    REL = 7
    ARI = 8
    UNARY = 9
    SEQ = 10
    ASSIGN = 11
    IF_STMT = 12
    WHILE_STMT = 13
    DOWHILE_STMT = 14
    TEMP = 15

class Node:
    labels = 0

    def __init__(self, t=NodeType.UNKNOWN):
        self.node_type = t

    def ToString(self):
        return ""

    @staticmethod
    def NewLabel():
        Node.labels += 1
        return Node.labels


class Statement(Node):
    def __init__(self, type_=NodeType.STMT):
        super().__init__(type_)

    def Gen(self):
        pass

class Expression(Node):
    def __init__(self, token=None, ntype=NodeType.EXPR, etype=ExprType.VOID):
        super().__init__(ntype)
        self.type = etype
        self.token = token

    def ToString(self):
        return self.token.lexeme if self.token else ""

    def Type(self):
        types = {ExprType.INT: "int", ExprType.FLOAT: "float", ExprType.BOOL: "bool", ExprType.VOID: "void"}
        return types.get(self.type, "void")
    
class Temp(Expression):
    count = 0

    def __init__(self, etype):
        super().__init__(None, NodeType.TEMP, etype)
        Temp.count += 1
        self.number = Temp.count

    def ToString(self):
        return f"t{self.number}"

class Constant(Expression):
    def __init__(self, etype, token):
        super().__init__(token, NodeType.CONSTANT, etype)


class Identifier(Expression):
    def __init__(self, etype, token):
        super().__init__(token, NodeType.IDENTIFIER, etype)

class Access(Expression):
    def __init__(self, etype, token, id_, expr):
        super().__init__(token, NodeType.ACCESS, etype)
        self.id = id_
        self.expr = expr

    def ToString(self):
        return f"{self.id.ToString()}[{self.expr.ToString()}]"

class Logical(Expression):
    def __init__(self, token, e1, e2):
        super().__init__(token, NodeType.LOG, ExprType.BOOL)
        self.expr1 = e1
        self.expr2 = e2
        # type check
        if self.expr1.type != ExprType.BOOL or self.expr2.type != ExprType.BOOL:
            raise SemanticErrorAST(f" Erro linha {globals.scanner.get_line()}: '{self.token.lexeme}' usado com operandos não booleanos ({self.expr1.ToString()}:{self.expr1.Type()}) ({self.expr2.ToString()}:{self.expr2.Type()})")

class Relational(Expression):
    def __init__(self, token, e1, e2):
        super().__init__(token, NodeType.REL, ExprType.BOOL)
        self.expr1 = e1
        self.expr2 = e2
        # type check
        if self.expr1.type != self.expr2.type:
            raise SemanticErrorAST(f"Erro linha {globals.scanner.get_line()}: '{self.token.lexeme}' usado com operandos de tipos diferentes ({self.expr1.ToString()}:{self.expr1.Type()}) ({self.expr2.ToString()}:{self.expr2.Type()})")

class Arithmetic(Expression):
    def __init__(self, etype, token, e1, e2):
        super().__init__(token, NodeType.ARI, etype)
        self.expr1 = e1
        self.expr2 = e2
        # type check
        if self.expr1.type != self.expr2.type:
            raise SemanticErrorAST(f"Erro linha {globals.scanner.get_line()}:  '{self.token.lexeme}' usado com operandos de tipos diferentes ({self.expr1.ToString()}:{self.expr1.Type()}) ({self.expr2.ToString()}:{self.expr2.Type()})")
class UnaryExpr(Expression):
    def __init__(self, etype, token, e):
        super().__init__(token, NodeType.UNARY, etype)
        self.expr = e
        # type check
        if token.tag == ord('!') and self.expr.type != ExprType.BOOL:
            raise SemanticErrorAST(f"Erro linha {globals.scanner.get_line()}: '{self.token.lexeme}' usado com operando não booleano ({self.expr.ToString()}:{self.expr.Type()})")
        if token.tag == ord('-') and self.expr.type not in (ExprType.INT, ExprType.FLOAT):
            raise SemanticErrorAST(f"Erro linha {globals.scanner.get_line()}: '{self.token.lexeme}' usado com operando não numérico ({self.expr.ToString()}:{self.expr.Type()})")

class Seq(Statement):
    def __init__(self, s, ss):
        super().__init__(NodeType.SEQ)
        self.stmt = s
        self.stmts = ss

    def Gen(self):
        self.stmt.Gen()
        if self.stmts:
            self.stmts.Gen()

class Assign(Statement):
    def __init__(self, i, e):
        super().__init__(NodeType.ASSIGN)
        self.id = i
        self.expr = e
        # type check
        if self.id.type != self.expr.type:
            raise SemanticErrorAST(f"Erro linha {globals.scanner.get_line()}: '=' usado com operandos de tipos diferentes ({self.id.ToString()}:{self.id.Type()}) ({self.expr.ToString()}:{self.expr.Type()})")

    def Gen(self):
        left = Lvalue(self.id)
        right = Rvalue(self.expr)
        print(f'\t{left.ToString()} = {right.ToString()}')

class If(Statement):
    def __init__(self, e, s):
        super().__init__(NodeType.IF_STMT)
        self.expr = e
        self.stmt = s
        # type check
        if self.expr.type != ExprType.BOOL:
            raise SemanticErrorAST(f"Erro linha {globals.scanner.get_line()}: expressão condicional '{self.expr.ToString()}' não booleana")
        self.after = Node.NewLabel()

    def Gen(self):
        n = Rvalue(self.expr)
        print(f"\tifFalse {n.ToString()} goto L{self.after}")
        self.stmt.Gen()
        print(f"L{self.after}:")

class While(Statement):
    def __init__(self, e, s):
        super().__init__(NodeType.WHILE_STMT)
        self.expr = e
        self.stmt = s
        # type check
        if self.expr.type != ExprType.BOOL:
            raise SemanticErrorAST(f"Erro linha {globals.scanner.get_line()}: expressão condicional '{self.expr.ToString()}' não booleana")
        self.start = Node.NewLabel()
        self.end = Node.NewLabel()

    def Gen(self):
        print(f"L{self.start}:")
        n = Rvalue(self.expr)
        print(f"\tifFalse {n.ToString()} goto L{self.end}")
        self.stmt.Gen()
        print(f"\tgoto L{self.start}")
        print(f"L{self.end}:")

class DoWhile(Statement):
    def __init__(self, s, e):
        super().__init__(NodeType.DOWHILE_STMT)
        self.stmt = s
        self.expr = e
        self.before = Node.NewLabel()

    def Gen(self):
        print(f"L{self.before}:")
        self.stmt.Gen()
        n = Rvalue(self.expr)
        print(f"\tifTrue {n.ToString()} goto L{self.before}")