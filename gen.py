import ast
from error import SyntaxError
import globals

def Lvalue(n):
    if n.node_type == ast.NodeType.IDENTIFIER:
        return n
    elif n.node_type == ast.NodeType.ACCESS:
        a = n
        return ast.Access(a.type, a.token, a.id, Rvalue(a.expr))
    else:
        raise SyntaxError(globals.scanner.get_line(), f"Expressão '{n.ToString()}' não possui valor-l")

def Rvalue(n):
    if n.node_type in (ast.NodeType.IDENTIFIER, ast.NodeType.CONSTANT):
        return n
    elif n.node_type == ast.NodeType.ARI:
        ari = n
        t = ast.Temp(ari.type)
        e1 = Rvalue(ari.expr1)
        e2 = Rvalue(ari.expr2)
        print(f'\t{t.ToString()} = {e1.ToString()} {ari.ToString()} {e2.ToString()}')
        return t
    elif n.node_type == ast.NodeType.REL:
        rel = n
        t = ast.Temp(rel.type)
        e1 = Rvalue(rel.expr1)
        e2 = Rvalue(rel.expr2)
        print(f'\t{t.ToString()} = {e1.ToString()} {rel.ToString()} {e2.ToString()}')
        return t
    elif n.node_type == ast.NodeType.LOG:
        log = n
        t = ast.Temp(log.type)
        e1 = Rvalue(log.expr1)
        e2 = Rvalue(log.expr2)
        print(f'\t{t.ToString()} = {e1.ToString()} {log.ToString()} {e2.ToString()}')
        return t
    elif n.node_type == ast.NodeType.UNARY:
        una = n
        t = ast.Temp(una.type)
        e = Rvalue(una.expr)
        print(f'\t{t.ToString()} = {una.ToString()}{e.ToString()}')
        return t
    elif n.node_type == ast.NodeType.ACCESS:
        access = n
        temp = ast.Temp(access.type)
        right = Lvalue(n)
        print(f'\t{temp.ToString()} = {right.ToString()}')
        return temp
    elif n.node_type == ast.NodeType.ASSIGN:
        acc = Lvalue(n)
        left = Lvalue(acc.id)
        right = Rvalue(acc.expr)
        print(f'\t{left.ToString()} = {right.ToString()}')
        return right
    else:
        raise SyntaxError(globals.scanner.lineno(), f"Expressão '{n.ToString()}' não possui valor-r")