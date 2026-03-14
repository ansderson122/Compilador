
# Neste arquivo estão as classes dos nós da AST (Abstract Syntax Tree)
# Cada nó tem um método get_ic() que gera o código intermediário correspondente a ele


# ===============================================================================
#                           NODES PARA LITERAIS
# ===============================================================================


class NumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'<NUMBER, {self.tok.value}>'

    def to_python(self, indent=0):
        return str(self.tok.value)


class StringNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'<STRING, {repr(self.tok.value)}>'

    def to_python(self, indent=0):
        return f'\"{self.tok.value}\"'


class BooleanNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return f'<BOOL, {self.tok.value}>'

    def to_python(self, indent=0):
        return 'True' if self.tok.value == 'true' else 'False'


# ===============================================================================
#                           NODES PARA IDENTIFICADORES
# ===============================================================================


class IdentifierNode:
    def __init__(self, tok):
        self.tok = tok
        self.name = tok.value
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end

    def __repr__(self):
        return f'<ID, {self.name}>'

    def to_python(self, indent=0):
        return self.name


# ===============================================================================
#                        NODES PARA OPERAÇÕES BINÁRIAS
# ===============================================================================
# as operações binárias são aquelas que envolvem dois operandos, como adição, subtração, multiplicação, divisão, etc.

class BinaryOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = left_node.pos_start
        self.pos_end = right_node.pos_end

    def __repr__(self):
        return f'({self.left_node} {self.op_tok} {self.right_node})'

    def to_python(self, ):
        # Mapeia operadores Mini-Lang para Python
        op_map = {
            'and': 'and',
            'or': 'or',
            '==': '==',
            '!=': '!=',
            '<': '<',
            '>': '>',
            '<=': '<=',
            '>=': '>=',
            '+': '+',
            '-': '-',
            '*': '*',
            '/': '/'
        }
        
        op_str = self.op_tok.value if hasattr(self.op_tok, 'value') else self.op_tok.type
        op = op_map.get(op_str, op_str)
        
        left = self.left_node.to_python(0)
        right = self.right_node.to_python(0)
        
        return f'({left} {op} {right})'


# ===============================================================================
#                        NODES PARA OPERAÇÕES UNÁRIAS
# ===============================================================================
# as operações unárias são aquelas que envolvem apenas um operando, como negação, incremento, etc.

class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = op_tok.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_tok} {self.node})'

    def to_python(self, indent=0):
        # Mapeia operadores Mini-Lang para Python
        op_map = {
            'not': 'not ',
            '+': '+',
            '-': '-'
        }
        
        op_str = self.op_tok.value if hasattr(self.op_tok, 'value') else self.op_tok.type
        op = op_map.get(op_str, op_str)
        
        operand = self.node.to_python(0)
        
        return f'({op}{operand})'


# ===============================================================================
#                   NODES PARA DECLARAÇÕES DE VARIÁVEIS
# ===============================================================================


class VariableDeclNode:
    def __init__(self, var_name, var_type, expression):
        self.var_name = var_name  # Token do identificador
        self.var_type = var_type   # Token do tipo (int, real, bool)
        self.expression = expression  # Nó da expressão

        self.pos_start = var_name.pos_start
        self.pos_end = expression.pos_end

    def __repr__(self):
        return f'<VAR_DECL, {self.var_name.value} : {self.var_type.value} = {self.expression}>'

    def to_python(self, indent=0):
        expr_code = self.expression.to_python(0)
        return f'{" " * indent}{self.var_name.value} = {expr_code}'


# ===============================================================================
#                      NODES PARA ATRIBUIÇÃO
# ===============================================================================

# A atribuição é diferente da declaração de variável, pois a variável já foi declarada antes e aqui estamos apenas atribuindo um novo valor a ela. Por exemplo:
class AssignmentNode:
    def __init__(self, var_name, expression):
        self.var_name = var_name  # Token do identificador
        self.expression = expression  # Nó da expressão

        self.pos_start = var_name.pos_start
        self.pos_end = expression.pos_end

    def __repr__(self):
        return f'<ASSIGN, {self.var_name.value} = {self.expression}>'

    def to_python(self, indent=0):
        expr_code = self.expression.to_python(0)
        return f'{" " * indent}{self.var_name.value} = {expr_code}'


# ===============================================================================
#                    NODES PARA PRINT E RETORNO
# ===============================================================================


class PrintNode:
    def __init__(self, string_node):
        self.string_node = string_node

        self.pos_start = string_node.pos_start
        self.pos_end = string_node.pos_end

    def __repr__(self):
        return f'<PRINT, {self.string_node}>'

    def to_python(self, indent=0):
        string_code = self.string_node.to_python(indent)
        return f'{" " * indent}print({string_code})'


class ReturnNode:
    def __init__(self, expression):
        self.expression = expression

        self.pos_start = expression.pos_start if expression else None
        self.pos_end = expression.pos_end if expression else None

    def __repr__(self):
        return f'<RETURN, {self.expression}>'

    def to_python(self, indent=0):
        if self.expression is None:
            return f'{" " * indent}return'
        
        expr_code = self.expression.to_python(0)
        return f'{" " * indent}return {expr_code}'


# ===============================================================================
#                  NODES PARA CONTROLE DE FLUXO
# ===============================================================================


class IfNode:
    def __init__(self, condition, if_block, else_block=None):
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block

        self.pos_start = condition.pos_start
        self.pos_end = else_block.pos_end if else_block else if_block.pos_end

    def __repr__(self):
        return f'<IF {self.condition} THEN {self.if_block} ELSE {self.else_block}>'

    def to_python(self, indent=0):
        """Retorna if/else como código Python"""
        code = ''
        cond = self.condition.to_python(0)
        code += f'{" " * indent}if {cond}:\n'
        code += self.if_block.to_python(indent + 4)
        
        if self.else_block:
            code += f'{" " * indent}else:\n'
            code += self.else_block.to_python(indent + 4)
        
        return code


class WhileNode:
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

        self.pos_start = condition.pos_start
        self.pos_end = block.pos_end

    def __repr__(self):
        return f'<WHILE {self.condition} DO {self.block}>'

    def to_python(self, indent=0):
        code = ''
        cond = self.condition.to_python(0)
        code += f'{" " * indent}while {cond}:\n'
        code += self.block.to_python(indent + 4)
        
        return code

# blockonode  
class BlockNode:
    def __init__(self, statements):
        self.statements = statements  # Lista de nós

        if statements:
            self.pos_start = statements[0].pos_start
            self.pos_end = statements[-1].pos_end
        else:
            self.pos_start = None
            self.pos_end = None

    def __repr__(self):
        return f'<BLOCK, {self.statements}>'

    def to_python(self, indent=0):
        code = ''
        for statement in self.statements:
            code += statement.to_python(indent)
            code += '\n'
        return code


# ===============================================================================
#                    NODES PARA FUNÇÕES
# ===============================================================================

# FunctionDeclNode representa a declaração de uma função, com seu nome, parâmetros, tipo de retorno e bloco de código
# FunctionCallNode representa a chamada de uma função, com seu nome e argumentos

class FunctionDeclNode:
    def __init__(self, func_name, params, return_type, block):
        self.func_name = func_name  # Token do nome
        self.params = params  # Lista de (nome, tipo)
        self.return_type = return_type  # Token do tipo
        self.block = block  # BlockNode

        self.pos_start = func_name.pos_start
        self.pos_end = block.pos_end

    def __repr__(self):
        params_str = ', '.join([f'{p[0].value}:{p[1].value}' for p in self.params])
        return f'<FUNC_DECL, {self.func_name.value}({params_str}) : {self.return_type.value} => {self.block}>'

    def to_python(self, indent=0):
        """Retorna declaração de função como código Python"""
        code = ''
        params_str = ', '.join([f'{p[0].value}' for p in self.params])
        code += f'{" " * indent}def {self.func_name.value}({params_str}):\n'
        code += self.block.to_python(indent + 4)
        
        return code


class FunctionCallNode:
    def __init__(self, func_name, args):
        self.func_name = func_name  # Token do nome
        self.args = args  # Lista de nós (argumentos)

        self.pos_start = func_name.pos_start
        self.pos_end = args[-1].pos_end if args else func_name.pos_end

    def __repr__(self):
        args_str = ', '.join([str(arg) for arg in self.args])
        return f'<FUNC_CALL, {self.func_name.value}({args_str})>'

    def to_python(self, indent=0):
        args = ', '.join([arg.to_python(0) for arg in self.args])
        return f'{self.func_name.value}({args})'


# ===============================================================================
#                    NODE PARA PROGRAMA
# ===============================================================================


class ProgramNode:
    def __init__(self, statements):
        self.statements = statements  # Lista de nós (funções e statements)

        if statements:
            self.pos_start = statements[0].pos_start
            self.pos_end = statements[-1].pos_end
        else:
            self.pos_start = None
            self.pos_end = None

    def __repr__(self):
        return f'<PROGRAM, {self.statements}>'

    def to_python(self, indent=0):
        code = ''
        for statement in self.statements:
            code += statement.to_python(0)
            code += '\n'
        return code