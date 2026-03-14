from .ast_nodes import *
from constants import *
from error import *


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.last_registered_advance_count = 0
        self.advance_count = 0
        self.to_reverse_count = 0

    # Registra um avanço no token e atualiza os contadores
    def register_advancement(self):
        self.last_registered_advance_count = 1
        self.advance_count += 1

    # Registra o resultado de uma regra de produção, atualizando o nó e o erron caso haja
    def register(self, res):
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    # Tenta registrar o resultado de uma regra de produção, mas se houver erro, armazena quantos avanços foram feitos para poder retroceder
    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    # Marca o resultado como sucesso, armazenando o nó resultante
    def success(self, node):
        self.node = node
        return self

    # Marca o resultado como falha, armazenando o erro se ainda não houver um erro registrado ou se nenhum avanço tiver sido feito
    def failure(self, error):
        if not self.error or self.last_registered_advance_count == 0:
            self.error = error
        return self
    

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    # Avança para o próximo token e atualiza o token atual
    def advance(self):
        self.tok_idx += 1
        self.update_current_tok()
        return self.current_tok

    # Permite retroceder o token para tentar outra regra de produção
    def reverse(self, amount=1):
        self.tok_idx -= amount
        self.update_current_tok()
        return self.current_tok

    # Atualiza o token atual com base no índice do token
    def update_current_tok(self):
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]

    # =================================================================================
    # Esse função é o ponto de entrada para o parser - chama a regra raiz do programa
    # Ela é chamada pelos testes para obter a AST completa do programa
    # current_tok é inicializado no construtor e atualizado por advance() e reverse()
    def parse(self):
        res = self.program()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                 "Token cannot appear after previous tokens"
            ))
        return res

    ###################################
    # PROGRAMA E ESTRUTURA BÁSICA
    ###################################

    def program(self):
        """
        <program> → <statement_list>
        Regra raiz - Retorna a árvore sintática completa
        """
        res = ParseResult()
        statements = []
        
        while self.current_tok.type != TT_EOF:
            if self.current_tok.type in (TT_SEMICOLON,):
                res.register_advancement()
                self.advance()
                continue
            
            stmt = res.register(self.statement())
            if res.error:
                return res
            
            if stmt:
                statements.append(stmt)
        
        return res.success(ProgramNode(statements))

    def statements(self):
        """
        <statement_list> → <statement> <statement_list> | ε
        Lê múltiplos statements
        """
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()

        while self.current_tok.type != TT_EOF:
            if self.current_tok.type in (TT_SEMICOLON,):
                res.register_advancement()
                self.advance()
                continue
            
            stmt = res.try_register(self.statement())
            if not stmt:
                self.reverse(res.to_reverse_count)
                break
            
            statements.append(stmt)

        return res.success(BlockNode(statements)) if statements else res.success(None)

    def statement(self):
        """
        <statement> → <variable_decl> ";"
                    | <assignment> ";"
                    | <print_statement> ";"
                    | <if_statement>
                    | <while_statement>
                    | <return_statement> ";"
                    | <function_decl>
                    | <block>
        Identifica qual tipo de statement
        """
        res = ParseResult()
        pos_start = self.current_tok.pos_start

        # Variable declaration: var ...
        if self.current_tok.type == TT_KEYWORD and self.current_tok.value == 'var':
            res.register_advancement()
            self.advance()
            stmt = res.register(self.variable_decl(pos_start))
            if res.error:
                return res
            
            if self.current_tok.type == TT_SEMICOLON:
                res.register_advancement()
                self.advance()
            return res.success(stmt)

        # Assignment: set ...
        if self.current_tok.type == TT_KEYWORD and self.current_tok.value == 'set':
            res.register_advancement()
            self.advance()
            stmt = res.register(self.assignment(pos_start))
            if res.error:
                return res
            
            if self.current_tok.type == TT_SEMICOLON:
                res.register_advancement()
                self.advance()
            return res.success(stmt)

        # Print statement: print ...
        if self.current_tok.type == TT_KEYWORD and self.current_tok.value == 'print':
            res.register_advancement()
            self.advance()
            stmt = res.register(self.print_statement(pos_start))
            if res.error:
                return res
            
            if self.current_tok.type == TT_SEMICOLON:
                res.register_advancement()
                self.advance()
            return res.success(stmt)

        # If statement: if ...
        if self.current_tok.type == TT_KEYWORD and self.current_tok.value == 'if':
            return self.if_statement()

        # While statement: while ...
        if self.current_tok.type == TT_KEYWORD and self.current_tok.value == 'while':
            return self.while_statement()

        # Return statement: return ...
        if self.current_tok.type == TT_KEYWORD and self.current_tok.value == 'return':
            res.register_advancement()
            self.advance()
            stmt = res.register(self.return_statement(pos_start))
            if res.error:
                return res
            
            if self.current_tok.type == TT_SEMICOLON:
                res.register_advancement()
                self.advance()
            return res.success(stmt)

        # Function declaration: def ...
        if self.current_tok.type == TT_KEYWORD and self.current_tok.value == 'def':
            return self.function_decl()

        # Block: { ...
        if self.current_tok.type == TT_LBRACE:
            return self.block()

        return res.success(None)

    def block(self):
        """
        <block> → "{" <statement_list> "}"
        Bloco de código entre chaves
        """
        res = ParseResult()
        pos_start = self.current_tok.pos_start

        if self.current_tok.type != TT_LBRACE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Esperado '{'"
            ))

        res.register_advancement()
        self.advance()

        statements = []
        while self.current_tok.type != TT_RBRACE and self.current_tok.type != TT_EOF:
            if self.current_tok.type in (TT_SEMICOLON,):
                res.register_advancement()
                self.advance()
                continue
            
            stmt = res.try_register(self.statement())
            if not stmt:
                self.reverse(res.to_reverse_count)
                break
            
            statements.append(stmt)

        pos_end = self.current_tok.pos_end

        if self.current_tok.type != TT_RBRACE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Esperado '}'"
            ))

        res.register_advancement()
        self.advance()

        return res.success(BlockNode(statements))

    ###################################
    # FUNÇÃO
    ###################################

    def function_decl(self):
        """
        <function_decl> → "def" <identifier> "(" <formal_params_opt> ")" ":" <type> <block>
        Declaração de função
        """
        res = ParseResult()
        pos_start = self.current_tok.pos_start

        if self.current_tok.type != TT_KEYWORD or self.current_tok.value != 'def':
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Esperado 'def'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Esperado identificador"
            ))

        func_name_tok = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_LPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Esperado '('"
            ))

        res.register_advancement()
        self.advance()

        params = res.register(self.formal_params_opt())
        if res.error:
            return res

        if self.current_tok.type != TT_RPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Esperado ')'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_COLON:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Esperado ':'"
            ))

        res.register_advancement()
        self.advance()

        return_type = res.register(self.type_())
        if res.error:
            return res

        block = res.register(self.block())
        if res.error:
            return res

        return res.success(FunctionDeclNode(func_name_tok, params, return_type, block))

    def formal_params_opt(self):
        """
        <formal_params_opt> → <formal_params> | ε
        Parâmetros formais opcionais
        """
        res = ParseResult()

        if self.current_tok.type == TT_RPAREN:
            return res.success([])

        return self.formal_params()

    def formal_params(self):
        """
        <formal_params> → <formal_param> <formal_params_rest>
        Lista de parâmetros formais
        """
        res = ParseResult()
        params = []

        param = res.register(self.formal_param())
        if res.error:
            return res
        params.append(param)

        rest_params = res.register(self.formal_params_rest())
        if res.error:
            return res
        params.extend(rest_params)

        return res.success(params)

    def formal_params_rest(self):
        """
        <formal_params_rest> → "," <formal_param> <formal_params_rest> | ε
        Resto dos parâmetros formais
        """
        res = ParseResult()
        params = []

        while self.current_tok.type == TT_COMMA:
            res.register_advancement()
            self.advance()

            param = res.register(self.formal_param())
            if res.error:
                return res
            params.append(param)

        return res.success(params)

    def formal_param(self):
        """
        <formal_param> → <identifier> ":" <type>
        Um parâmetro formal (nome e tipo)
        """
        res = ParseResult()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Esperado identificador"
            ))

        param_name = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_COLON:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Esperado ':'"
            ))

        res.register_advancement()
        self.advance()

        param_type = res.register(self.type_())
        if res.error:
            return res

        return res.success((param_name, param_type))

    ###################################
    # CONTROLADOR DE FLUXO
    ###################################

    def if_statement(self):
        """
        <if_statement> → "if" "(" <expression> ")" <block> <else_opt>
        Comando if com else opcional
        """
        res = ParseResult()
        pos_start = self.current_tok.pos_start

        if self.current_tok.type != TT_KEYWORD or self.current_tok.value != 'if':
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Esperado 'if'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_LPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Esperado '('"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expression())
        if res.error:
            return res

        if self.current_tok.type != TT_RPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Esperado ')'"
            ))

        res.register_advancement()
        self.advance()

        if_block = res.register(self.block())
        if res.error:
            return res

        else_block = res.register(self.else_opt())
        if res.error:
            return res

        return res.success(IfNode(condition, if_block, else_block))

    def else_opt(self):
        """
        <else_opt> → "else" <block> | ε
        Bloco else opcional
        """
        res = ParseResult()

        if self.current_tok.type == TT_KEYWORD and self.current_tok.value == 'else':
            res.register_advancement()
            self.advance()

            else_block = res.register(self.block())
            if res.error:
                return res

            return res.success(else_block)

        return res.success(None)

    def while_statement(self):
        """
        <while_statement> → "while" "(" <expression> ")" <block>
        Loop while
        """
        res = ParseResult()
        pos_start = self.current_tok.pos_start

        if self.current_tok.type != TT_KEYWORD or self.current_tok.value != 'while':
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Esperado 'while'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_LPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Esperado '('"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expression())
        if res.error:
            return res

        if self.current_tok.type != TT_RPAREN:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Esperado ')'"
            ))

        res.register_advancement()
        self.advance()

        block = res.register(self.block())
        if res.error:
            return res

        return res.success(WhileNode(condition, block))

    ###################################
    # DECLARAÇÕES E STATEMENTS
    ###################################

    def variable_decl(self, pos_start):
        """
        <variable_decl> → "var" <identifier> ":" <type> "=" <expression>
        Declaração de variável
        """
        res = ParseResult()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Esperado identificador"
            ))

        var_name = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_COLON:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Esperado ':'"
            ))

        res.register_advancement()
        self.advance()

        var_type = res.register(self.type_())
        if res.error:
            return res

        if self.current_tok.type != TT_EQ:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Esperado '='"
            ))

        res.register_advancement()
        self.advance()

        expr = res.register(self.expression())
        if res.error:
            return res

        return res.success(VariableDeclNode(var_name, var_type, expr))

    def assignment(self, pos_start):
        """
        <assignment> → "set" <identifier> "=" <expression>
        Atribuição a variável existente
        """
        res = ParseResult()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Esperado identificador"
            ))

        var_name = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_EQ:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Esperado '='"
            ))

        res.register_advancement()
        self.advance()

        expr = res.register(self.expression())
        if res.error:
            return res

        return res.success(AssignmentNode(var_name, expr))

    def print_statement(self, pos_start):
        """
        <print_statement> → "print" <string_literal>
        Statement de impressão
        """
        res = ParseResult()

        if self.current_tok.type != TT_STRING:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Esperado string"
            ))

        string_tok = self.current_tok
        res.register_advancement()
        self.advance()

        string_node = StringNode(string_tok)
        return res.success(PrintNode(string_node))

    def return_statement(self, pos_start):
        """
        <return_statement> → "return" <expression>
        Statement de retorno
        """
        res = ParseResult()

        if self.current_tok.type == TT_SEMICOLON or self.current_tok.type == TT_EOF:
            return res.success(ReturnNode(None))

        expr = res.register(self.expression())
        if res.error:
            return res

        return res.success(ReturnNode(expr))

    def type_(self):
        """
        <type> → "int" | "real" | "bool" | "void" | "string"
        Tipo de dado
        """
        res = ParseResult()

        if self.current_tok.type == TT_KEYWORD and self.current_tok.value in ('int', 'real', 'bool', 'void', 'string'):
            type_tok = self.current_tok
            res.register_advancement()
            self.advance()
            return res.success(type_tok)

        return res.failure(InvalidSyntaxError(
            self.current_tok.pos_start, self.current_tok.pos_end,
            "Esperado tipo (int, real, bool, void, string)"
        ))

    ###################################
    # EXPRESSÕES
    ###################################

    def expression(self):
        """
        <expression> → <simple_expression> <expression_rest>
        Expressão (precedência baixa - operadores relacionais)
        """
        res = ParseResult()

        left = res.register(self.simple_expression())
        if res.error:
            return res

        return self.expression_rest(left)

    def expression_rest(self, left):
        """
        <expression_rest> → <relational_op> <simple_expression> <expression_rest> | ε
        Continuação de expressão com operadores relacionais
        """
        res = ParseResult()

        while self.current_tok.type in (TT_LT, TT_GT, TT_EE, TT_NE, TT_LTE, TT_GTE):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            right = res.register(self.simple_expression())
            if res.error:
                return res

            left = BinaryOpNode(left, op_tok, right)

        return res.success(left)

    def simple_expression(self):
        """
        <simple_expression> → <term> <simple_expression_rest>
        Expressão simples (precedência média - operadores aditivos)
        """
        res = ParseResult()

        left = res.register(self.term())
        if res.error:
            return res

        return self.simple_expression_rest(left)

    def simple_expression_rest(self, left):
        """
        <simple_expression_rest> → <additive_op> <term> <simple_expression_rest> | ε
        Continuação com operadores aditivos (+, -, or)
        """
        res = ParseResult()

        while (self.current_tok.type in (TT_PLUS, TT_MINUS) or
               (self.current_tok.type == TT_KEYWORD and self.current_tok.value == 'or')):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            right = res.register(self.term())
            if res.error:
                return res

            left = BinaryOpNode(left, op_tok, right)

        return res.success(left)

    def term(self):
        """
        <term> → <factor> <term_rest>
        Termo (precedência alta - operadores multiplicativos)
        """
        res = ParseResult()

        left = res.register(self.factor())
        if res.error:
            return res

        return self.term_rest(left)

    def term_rest(self, left):
        """
        <term_rest> → <multiplicative_op> <factor> <term_rest> | ε
        Continuação com operadores multiplicativos (*, /, and)
        """
        res = ParseResult()

        while (self.current_tok.type in (TT_MUL, TT_DIV) or
               (self.current_tok.type == TT_KEYWORD and self.current_tok.value == 'and')):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            right = res.register(self.factor())
            if res.error:
                return res

            left = BinaryOpNode(left, op_tok, right)

        return res.success(left)

    def factor(self):
        """
        <factor> → <literal>
                 | <identifier>
                 | <function_call>
                 | <sub_expression>
                 | <unary>
        Fator (maior precedência)
        """
        res = ParseResult()
        tok = self.current_tok

        # Literal: número
        if tok.type in (TT_INT, TT_REAL):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        # Literal: string
        if tok.type == TT_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))

        # Literal: booleano ou identificador/função
        if tok.type == TT_KEYWORD:
            if tok.value in ('true', 'false'):
                res.register_advancement()
                self.advance()
                return res.success(BooleanNode(tok))

        # Identificador ou chamada de função
        if tok.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()

            # Verifica se é função
            if self.current_tok.type == TT_LPAREN:
                res.register_advancement()
                self.advance()

                args = res.register(self.actual_params_opt())
                if res.error:
                    return res

                if self.current_tok.type != TT_RPAREN:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Esperado ')'"
                    ))

                res.register_advancement()
                self.advance()

                return res.success(FunctionCallNode(tok, args))

            return res.success(IdentifierNode(tok))

        # Subexpressão: (...)
        if tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()

            expr = res.register(self.expression())
            if res.error:
                return res

            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Esperado ')'"
                ))

            res.register_advancement()
            self.advance()

            return res.success(expr)

        # Operador unário
        if tok.type in (TT_PLUS, TT_MINUS) or (tok.type == TT_KEYWORD and tok.value == 'not'):
            return self.unary()

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Esperado número, string, identificador, '(' ou operador unário"
        ))

    def unary(self):
        """
        <unary> → <unary_op> <expression>
        Operador unário (+, -, not)
        """
        res = ParseResult()

        op_tok = res.register(self.unary_op())
        if res.error:
            return res

        expr = res.register(self.expression())
        if res.error:
            return res

        return res.success(UnaryOpNode(op_tok, expr))

    def unary_op(self):
        """
        <unary_op> → "+" | "-" | "not"
        Operador unário
        """
        res = ParseResult()
        tok = self.current_tok

        if tok.type == TT_PLUS:
            res.register_advancement()
            self.advance()
            return res.success(tok)

        if tok.type == TT_MINUS:
            res.register_advancement()
            self.advance()
            return res.success(tok)

        if tok.type == TT_KEYWORD and tok.value == 'not':
            res.register_advancement()
            self.advance()
            return res.success(tok)

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Esperado operador unário (+, -, not)"
        ))

    ###################################
    # PARÂMETROS DE FUNÇÃO
    ###################################

    def actual_params_opt(self):
        """
        <actual_params_opt> → <actual_params> | ε
        Parâmetros reais opcionais
        """
        res = ParseResult()

        if self.current_tok.type == TT_RPAREN:
            return res.success([])

        return self.actual_params()

    def actual_params(self):
        """
        <actual_params> → <expression> <actual_params_rest>
        Lista de parâmetros reais
        """
        res = ParseResult()
        params = []

        expr = res.register(self.expression())
        if res.error:
            return res
        params.append(expr)

        rest_params = res.register(self.actual_params_rest())
        if res.error:
            return res
        params.extend(rest_params)

        return res.success(params)

    def actual_params_rest(self):
        """
        <actual_params_rest> → "," <expression> <actual_params_rest> | ε
        Resto dos parâmetros reais
        """
        res = ParseResult()
        params = []

        while self.current_tok.type == TT_COMMA:
            res.register_advancement()
            self.advance()

            expr = res.register(self.expression())
            if res.error:
                return res
            params.append(expr)

        return res.success(params)