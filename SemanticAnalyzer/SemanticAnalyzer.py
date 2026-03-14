
from SemanticAnalyzer.symbol_table import escope
from Parser.ast_nodes import (
    ProgramNode, BlockNode, NumberNode, StringNode, BooleanNode,
    IdentifierNode, BinaryOpNode, UnaryOpNode, VariableDeclNode,
    AssignmentNode, PrintNode, ReturnNode, IfNode, WhileNode,
    FunctionDeclNode, FunctionCallNode
)


class SemanticAnalyzer:
    """
    Analisador Semântico para a linguagem Mini-Lang.
    Verifica tipos, declarações de variáveis e funções.
    """

    def __init__(self):
        self.scope = escope()
        self.scope.push_stack()  # escopo global
    
    def analyze(self, node):
        """Ponto de entrada para análise semântica"""
        return self.visit(node)
    
    def visit(self, node):
        """Dispatcher que chama o método correto baseado no tipo do nó"""
        if node is None:
            return None
            
        if isinstance(node, ProgramNode):
            return self.visit_program(node)
        elif isinstance(node, BlockNode):
            return self.visit_block(node)
        elif isinstance(node, VariableDeclNode):
            return self.visit_var_decl(node)
        elif isinstance(node, AssignmentNode):
            return self.visit_assignment(node)
        elif isinstance(node, PrintNode):
            return self.visit_print(node)
        elif isinstance(node, ReturnNode):
            return self.visit_return(node)
        elif isinstance(node, IfNode):
            return self.visit_if(node)
        elif isinstance(node, WhileNode):
            return self.visit_while(node)
        elif isinstance(node, FunctionDeclNode):
            return self.visit_func_decl(node)
        elif isinstance(node, FunctionCallNode):
            return self.visit_func_call(node)
        elif isinstance(node, BinaryOpNode):
            return self.visit_binary_op(node)
        elif isinstance(node, UnaryOpNode):
            return self.visit_unary_op(node)
        elif isinstance(node, NumberNode):
            return self.visit_number(node)
        elif isinstance(node, StringNode):
            return self.visit_string(node)
        elif isinstance(node, BooleanNode):
            return self.visit_boolean(node)
        elif isinstance(node, IdentifierNode):
            return self.visit_identifier(node)
        else:
            raise Exception(f"Nó desconhecido: {type(node)}")
    
    # ========== PROGRAMA ==========
    def visit_program(self, node: ProgramNode):
        """Visita o programa e todos seus statements"""
        for statement in node.statements:
            self.visit(statement)
    
    # ========== BLOCOS ==========
    def visit_block(self, node: BlockNode):
        """Visita um bloco de statements"""
        for statement in node.statements:
            self.visit(statement)
    
    # ========== DECLARAÇÕES DE VARIÁVEIS ==========
    def visit_var_decl(self, node: VariableDeclNode):
        """Verifica declaração de variável e tipo"""
        var_name = node.var_name.value
        var_type = node.var_type.value
        
        # Verifica o tipo da expressão
        expr_type = self.visit(node.expression)
        
        # Verifica compatibilidade de tipos
        if not self._is_type_compatible(expr_type, var_type):
            raise Exception(
                f"Erro de tipo em '{var_name}': "
                f"esperava {var_type}, obteve {expr_type}"
            )
        
        # Adiciona à tabela de símbolos
        self.scope.current_table().add_symbol(
            var_name,
            None, # Valor inicial é None, pois ainda não foi atribuído
            var_type
        )
    
    # ========== ATRIBUIÇÃO ==========
    def visit_assignment(self, node: AssignmentNode):
        """Verifica atribuição a uma variável"""
        var_name = node.var_name.value
        
        # Verifica se variável foi declarada
        if not self.scope.verify_symbol(var_name):
            raise Exception(f"Variável '{var_name}' não foi declarada")
        
        # Obtém o tipo da variável
        var_type = self.scope.current_table().get_symbol(var_name)["Type"]
        
        # Verifica o tipo da expressão
        expr_type = self.visit(node.expression)
        
        # Verifica compatibilidade de tipos
        if not self._is_type_compatible(expr_type, var_type):
            raise Exception(
                f"Erro de tipo em atribuição a '{var_name}': "
                f"esperava {var_type}, obteve {expr_type}"
            )
    
    # ========== PRINT ==========
    def visit_print(self, node: PrintNode):
        """Verifica print statement"""
        # Valida a expressão a ser impressa
        return self.visit(node.expression)
    
    # ========== RETURN ==========
    def visit_return(self, node: ReturnNode):
        """Verifica return statement"""
        if node.expression:
            return self.visit(node.expression)
        return None
    
    # ========== CONTROLE DE FLUXO ==========
    def visit_if(self, node: IfNode ):
        """Verifica if statement"""
        # Verifica que a condição é booleana
        cond_type = self.visit(node.condition)
        if cond_type != "bool":
            raise Exception(
                f"Erro: condição do 'if' deve ser 'bool', obteve '{cond_type}'"
            )
        
        # Visita os blocos
        self.visit(node.if_block)
        if node.else_block:
            self.visit(node.else_block)
    
    def visit_while(self, node: WhileNode):
        """Verifica while statement"""
        # Verifica que a condição é booleana
        cond_type = self.visit(node.condition)
        if cond_type != "bool":
            raise Exception(
                f"Erro: condição do 'while' deve ser 'bool', obteve '{cond_type}'"
            )
        
        # Visita o bloco
        self.visit(node.block)
    
    # ========== FUNÇÕES ==========
    def visit_func_decl(self, node: FunctionDeclNode):
        """Verifica declaração de função"""
        func_name = node.func_name.value
        return_type = node.return_type.value
        
        # Adiciona função à tabela de símbolos
        self.scope.current_table().add_symbol(
            func_name,
            {
                "params": node.params,
                "return_type": return_type,
                "body": node.block
            },
            "function"
        )
        
        # Cria novo escopo para parâmetros e corpo da função
        self.scope.push_stack()
        
        # Adiciona parâmetros ao novo escopo
        for param_name, param_type in node.params:
            self.scope.current_table().add_symbol(
                param_name.value,
                None,
                param_type.value
            )
        
        # Visita o corpo da função
        self.visit(node.block)
        
        # Sai do escopo da função
        self.scope.pop_stack()
    
    def visit_func_call(self, node: FunctionCallNode):
        """Verifica chamada de função"""
        func_name = node.func_name.value
        
        # Verifica se função foi declarada
        if not self.scope.verify_symbol(func_name):
            raise Exception(f"Função '{func_name}' não foi declarada")
        
        func_info = self.scope.get_symbol(func_name)
        
        # Verifica se é realmente uma função
        if func_info["Type"] != "function":
            raise Exception(f"'{func_name}' não é uma função")
        
        # Verifica número de argumentos
        expected_args = len(func_info["Value"]["params"])
        actual_args = len(node.args)
        
        if expected_args != actual_args:
            raise Exception(
                f"Função '{func_name}' espera {expected_args} argumentos, "
                f"mas recebeu {actual_args}"
            )
        
        # Verifica tipos dos argumentos
        for i, arg in enumerate(node.args):
            arg_type = self.visit(arg)
            param_type = func_info["Value"]["params"][i][1].value
            
            if not self._is_type_compatible(arg_type, param_type):
                raise Exception(
                    f"Argumento {i + 1} da função '{func_name}': "
                    f"esperava {param_type}, obteve {arg_type}"
                )
        
        # Retorna o tipo de retorno da função
        return func_info["Value"]["return_type"]
    
    # ========== OPERAÇÕES ==========
    def visit_binary_op(self, node: BinaryOpNode):
        """Verifica operação binária"""
        left_type = self.visit(node.left_node)
        right_type = self.visit(node.right_node)
        
        # Extrai o operador - tenta 'value' primeiro, depois 'type'
        if hasattr(node.op_tok, 'value') and node.op_tok.value:
            op = node.op_tok.value
        elif hasattr(node.op_tok, 'type'):
            op = node.op_tok.type
        else:
            op = str(node.op_tok)
           
        # Operadores aritméticos: +, -, *, /
        if op in ['PLUS', 'MINUS', 'MUL', 'DIV']:
            if left_type not in ['int', 'real'] or right_type not in ['int', 'real']:
                raise Exception(
                    f"Erro de tipo em '{op}': "
                    f"operandos devem ser numéricos, obteve {left_type} e {right_type}"
                )
            # Se um é real, retorna real; senão retorna int
            return 'real' if left_type == 'real' or right_type == 'real' else 'int'
        
        # Operadores lógicos: and, or
        elif op in ['and','or','AND', 'OR']:
            if left_type != 'bool' or right_type != 'bool':
                raise Exception(
                    f"Erro de tipo em '{op}': "
                    f"operandos devem ser booleanos"
                )
            return 'bool'
        
        # Operadores de comparação: ==, !=, <, >, <=, >=
        elif op in ['EE', 'NE', 'LT', 'GT', 'LTE', 'GTE']:
            if left_type not in ['int', 'real'] or right_type not in ['int', 'real']:
                raise Exception(
                    f"Erro de tipo em '{op}': "
                    f"operandos devem ser numéricos"
                )
            return 'bool'
        
        else:
            raise Exception(f"Operador desconhecido: {op}")
    
    def visit_unary_op(self, node: UnaryOpNode):
        """Verifica operação unária"""
        operand_type = self.visit(node.node)
        
        # Extrai o operador - tenta 'value' primeiro, depois 'type'
        if hasattr(node.op_tok, 'value') and node.op_tok.value:
            op = node.op_tok.value
        elif hasattr(node.op_tok, 'type'):
            op = node.op_tok.type
        else:
            op = str(node.op_tok)
        
        # Mapeia tipos de token para operadores
        op_map = {
            'PLUS': '+', 'MINUS': '-', 'NOT': 'not'
        }
        op = op_map.get(op, op)
        
        if op in ['not', 'NOT']:
            if operand_type != 'bool':
                raise Exception(
                    f"Erro de tipo em 'not': operando deve ser booleano, obteve {operand_type}"
                )
            return 'bool'
        elif op in ['+', '-', 'PLUS', 'MINUS']:
            if operand_type not in ['int', 'real']:
                raise Exception(
                    f"Erro de tipo em '{op}': operando deve ser numérico, obteve {operand_type}"
                )
            return operand_type
        else:
            raise Exception(f"Operador unário desconhecido: {op}")
    
    # ========== LITERAIS E IDENTIFICADORES ==========
    def visit_number(self, node: NumberNode):
        """Retorna o tipo de um número"""
        # Verifica se é ponto flutuante ou inteiro
        if '.' in str(node.tok.value):
            return 'real'
        return 'int'
    
    def visit_string(self, node: StringNode):
        """Retorna o tipo de uma string"""
        return 'string'
    
    def visit_boolean(self, node: BooleanNode):
        """Retorna o tipo de um booleano"""
        return 'bool'
    
    def visit_identifier(self, node: IdentifierNode):
        """Verifica identificador e retorna seu tipo"""
        var_name = node.name
        
        if not self.scope.verify_symbol(var_name):
            raise Exception(f"Variável '{var_name}' não foi declarada")
        
        return self.scope.current_table().get_symbol(var_name)["Type"]
    
    # ========== FUNÇÕES AUXILIARES ==========
    def _is_type_compatible(self, from_type: str, to_type: str):
        """Verifica se um tipo é compatível com outro"""
        if from_type == to_type:
            return True
        
        # int é compatível com real em algumas linguagens
        # Neste caso, sendo Mini-Lang, vamos ser restritivo
        return False