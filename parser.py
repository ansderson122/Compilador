from lexer import *
from symtable import *
from ast import *
from error import SyntaxError
import globals

# Definimos uma exceção personalizada para evitar confusão 
# com o "SyntaxError" nativo do Python
class ParseError(Exception):
    def __init__(self, message="Erro de sintaxe"):
        self.message = message
        super().__init__(self.message)

class Parser:
    def __init__(self):
        self._sym_table = SymTable()
        self.lookahead = None

    def start(self):
        self.lookahead = globals.scanner.scan()
        return self.program()
    
    @staticmethod
    def lineno():
        return globals.scanner.get_line()

    def program(self):

        # program -> int main() block

        # verifica erros na declaracao do main
        # program -> int main() block
        if not self.match(TAG.TYPE.value):
            raise SyntaxError(self.lineno(), "'int' esperado")
        if not self.match(TAG.MAIN.value):
            raise SyntaxError(self.lineno(), "'main' esperado")
        if not self.match(ord('(')):
            raise SyntaxError(self.lineno(), "'(' esperado")
        if not self.match(ord(')')):
            raise SyntaxError(self.lineno(), "')' esperado")
        return self.block()
    
    def block(self):
        # block -> { decls stmts }
        if not self.match(ord('{')):
            print(self.lookahead.lexeme)
            raise ParseError(f"Erro na linha {self.lineno()}: era esperado fechamento de chaves no início do bloco.")

        # ==== ação semântica ====
        # 1. salva tabela atual
        saved_table = self._sym_table

        # 2. cria nova tabela aninhada
        self._sym_table = SymTable(prev=saved_table)

        self.decls()
        sts = self.stmts()

        if not self.match(ord('}')):
            raise ParseError(f"Erro na linha {self.lineno()}:" 
                             "era esperado '}' no final do bloco.")
        

        # ==== ação semântica ====
        # restaura tabela anterior
        self._sym_table = saved_table
        del saved_table

        return sts
    
    def decls(self):
        # decls -> decl decls | ϵ
        # decl -> type id index;
        # index -> [num] | ϵ

        while self.lookahead.tag == TAG.TYPE.value:
            
            # salva o nome do tipo do identificador
            type = self.lookahead.lexeme
            if not self.match(TAG.TYPE.value):
                raise ParseError(f"Erro na linha {self.lineno()}:" 
                                 " era esperado um tipo de variável.")

            # salva o nome do identificador
            name = self.lookahead.lexeme
            if not self.match(TAG.ID.value):
                raise ParseError(f"Erro na linha {self.lineno()}:" 
                                 " era esperado um identificador.")

            s = Symbol(name, type)

            # insere a variável na tabela de símbolos
            if not self._sym_table.insert(name,s):
                raise ParseError(f"Erro na linha {self.lineno()}:" 
                                 f" variável '{name}' já declarada no escopo atual.")
            
            # verifica se é um array
            if self.match(ord('[')):
                # verifica se o número entre colchetes é inteiro
                if not self.match(TAG.INTEGER.value):
                    raise ParseError(f"Erro na linha {self.lineno()}:" 
                                     " era esperado um número inteiro '['.")
                
                # verifica se fecha o colchete
                if not self.match(ord(']')):
                    raise ParseError(f"Erro na linha {self.lineno()}:" 
                                     " era esperado ']' após tamanho do array.")

            
            # verifica a presença do ponto e virgula
            if not self.match(ord(';')):
                raise ParseError(f"Erro na linha {self.lineno()}:" 
                                 " era esperado ';' após declaração.")


    def stmt(self):
        # stmt -> local = bool;
        #      | if (bool) stmt
        #      | while (bool) stmt
        #      | do stmt while (bool);
        #      | block

        if self.lookahead.tag == TAG.ID.value:
            left_expr = self.local()
            if not self.match(ord('=')):
                raise ParseError(f"Erro na linha {self.lineno()}:" 
                                 " era esperado '=' em atribuição.")
            right_expr = self.Bool()
            stmt = Assign(left_expr,right_expr)
            if not self.match(ord(';')):
                raise ParseError(f"Erro na linha {self.lineno()}:" 
                                 " era esperado ';' após expressão.")
            return stmt
        elif self.lookahead.tag == TAG.IF.value:
            self.match(TAG.IF.value)
            if not self.match(ord('(')):
                raise ParseError(f"Erro na linha {self.lineno()}:" 
                                 " era esperado '(' após 'if'.")
            condition = self.Bool()
            
            if not self.match(ord(')')):
                raise ParseError(f"Erro na linha {self.lineno()}:" 
                                 " era esperado ')' após condição.")
            then_stmt = self.stmt()
            stmt = If(condition, then_stmt)
            return stmt
        elif self.lookahead.tag == TAG.WHILE.value:
            self.match(TAG.WHILE.value)
            if not self.match(ord('(')):
                raise ParseError(f"Erro na linha {self.lineno()}:" 
                                 " era esperado '(' após 'while'.")
            condition = self.Bool()
            if not self.match(ord(')')):
                raise ParseError(f"Erro na linha {self.lineno()}:" 
                                 " era esperado ')' após condição.")
            body_stmt = self.stmt()
            stmt = While(condition, body_stmt)
            return stmt
        elif self.lookahead.tag == TAG.DO.value:
            self.match(TAG.DO.value)
            body_stmt = self.stmt()
            if not self.match(TAG.WHILE.value):
                raise ParseError(f"Erro na linha {self.lineno()}:" 
                                 " era esperado 'while' após 'do'.")

            if not self.match(ord('(')):
                raise ParseError(f"Erro na linha {self.lineno()}:" 
                                 " era esperado '(' após 'while'.")
            condition = self.Bool()
            if not self.match(ord(')')):
                raise ParseError(f"Erro na linha {self.lineno()}:" 
                                 " era esperado ')' após condição.")
            if not self.match(ord(';')):
                raise ParseError(f"Erro na linha {self.lineno()}:" 
                                 " era esperado ';' após expressão.")
            stmt = DoWhile(body_stmt, condition)
            return stmt
        elif self.lookahead.tag == ord('{'):
            return self.block()
        else:
            raise ParseError(f"Erro na linha {self.lineno()}:" 
                             " declaração inválida.")

    def stmts(self):
        # stmts -> stmt stmts | ϵ

        seq = None

        if self.lookahead.tag in (TAG.ID.value, TAG.IF.value, TAG.WHILE.value, TAG.DO.value, ord('{')):
            st = self.stmt()
            sts = self.stmts()
            seq = Seq(st, sts)
        return seq
    
    def local(self):
        # local -> id
        name = self.lookahead.lexeme
        tok = self.lookahead
        self.match(TAG.ID.value)
        symb = self._sym_table.find(name)
        if symb is None:
            raise ParseError(f"Erro na linha {self.lineno()}:" 
                             f" variável '{name}' não declarada.")
        etype = ExprType.VOID
        if symb.type == "int":
            etype = ExprType.INT
        elif symb.type == "float":
            etype = ExprType.FLOAT
        elif symb.type == "bool":
            etype = ExprType.BOOL
        id = Identifier(etype, tok)

        if self.match(ord('[')):
            expr = self.Bool()
            if not self.match(ord(']')):
                raise ParseError(f"Erro na linha {self.lineno()}:" 
                                 " era esperado ']' após índice do array.")
            return Access(etype, Token(ord('['), '['), id, expr)
        return id
    
    def Bool(self):
        # bool -> join (|| join)*
        expr = self.join()
        while self.lookahead.tag == TAG.OR.value:
            tok = self.lookahead
            self.match(TAG.OR.value)
            expr2 = self.join()
            expr = Logical(tok, expr, expr2)
        return expr
    
    def join(self):
        # join -> equality (&& equality)*
        expr = self.equality()
        while self.lookahead.tag == TAG.AND.value:
            tok = self.lookahead
            self.match(TAG.AND.value)
            expr2 = self.equality()
            expr = Logical(tok, expr, expr2)
        return expr
    
    def equality(self):
        # equality -> rel ((==|!=) rel)*
        expr = self.rel()
        while self.lookahead.tag in (TAG.EQ.value, TAG.NEQ.value):
            tok = self.lookahead
            self.match(self.lookahead.tag)
            expr2 = self.rel()
            expr = Relational(tok, expr, expr2)
        return expr
    
    def rel(self):
        # rel -> ari ((<|<=|>|>=) ari)*
        expr = self.ari()
        while self.lookahead.tag in (ord('<'), ord('>'), TAG.LTE.value, TAG.GTE.value):
            tok = self.lookahead
            self.match(self.lookahead.tag)
            expr2 = self.ari()
            expr = Relational(tok, expr, expr2)
        return expr
    
    def ari(self):
        # ari -> term ((+|-) term)*
        expr = self.term()
        while self.lookahead.tag in (ord('+'), ord('-')):
            tok = self.lookahead
            self.match(self.lookahead.tag)
            expr2 = self.term()
            etype = ExprType.INT if expr.type == ExprType.INT else ExprType.FLOAT
            expr = Arithmetic(etype, tok, expr, expr2)
        return expr
    
    def term(self):
        # term -> unary ((*|/) unary)*
        expr = self.unary()
        while self.lookahead.tag in (ord('*'), ord('/')):
            tok = self.lookahead
            self.match(self.lookahead.tag)
            expr2 = self.unary()
            etype = ExprType.INT if expr.type == ExprType.INT else ExprType.FLOAT
            expr = Arithmetic(etype, tok, expr, expr2)
        return expr

    def unary(self):
        # unary -> ! unary | - unary | factor
        if self.lookahead.tag == ord('!'):
            tok = self.lookahead
            self.match(ord('!'))
            expr = self.unary()
            return UnaryExpr(ExprType.BOOL, tok, expr)
        elif self.lookahead.tag == ord('-'):
            tok = self.lookahead
            self.match(ord('-'))
            expr = self.unary()
            etype = ExprType.INT if expr.type == ExprType.INT else ExprType.FLOAT
            return UnaryExpr(etype, tok, expr)
        else:
            return self.factor()

    def factor(self):
        # factor -> ( bool ) | num | true | false | id [ bool ] | id
        if self.match(ord('(')):
            expr = self.Bool()
            if not self.match(ord(')')):
                raise ParseError(f"Erro na linha {self.lineno()}: esperado ) no lugar de '{self.lookahead.lexeme}'")
            return expr
        elif self.lookahead.tag == TAG.INTEGER.value:
            tok = self.lookahead
            self.match(TAG.INTEGER.value)
            return Constant(ExprType.INT, tok)
        elif self.lookahead.tag == TAG.FLOATING.value:
            tok = self.lookahead
            self.match(TAG.FLOATING.value)
            return Constant(ExprType.FLOAT, tok)
        elif self.lookahead.tag == TAG.TRUE.value:
            tok = self.lookahead
            self.match(TAG.TRUE.value)
            return Constant(ExprType.BOOL, tok)
        elif self.lookahead.tag == TAG.FALSE.value:
            tok = self.lookahead
            self.match(TAG.FALSE.value)
            return Constant(ExprType.BOOL, tok)
        elif self.lookahead.tag == TAG.ID.value:
            name = self.lookahead.lexeme
            tok = self.lookahead
            self.match(TAG.ID.value)
            symb = self._sym_table.find(name)
            if not symb:
                raise ParseError(self.lineno(), f"variável '{name}' não declarada")
            if symb.type == "int":
                etype = ExprType.INT
            elif symb.type == "float":
                etype = ExprType.FLOAT
            elif symb.type == "bool":
                etype = ExprType.BOOL
            else:
                raise ParseError(self.lineno(), f"tipo desconhecido '{symb.type}'")
            id_ = Identifier(etype, tok)
            if self.match(ord('[')):
                expr = self.Bool()
                if not self.match(ord(']')):
                    raise ParseError(f"Erro na linha {self.lineno()}: esperado ] no lugar de '{self.lookahead.lexeme}'")
                return Access(etype, Token(ord('['), "["), id_, expr)
            return id_
        else:
            raise ParseError(f"Erro na linha {self.lineno()}: fator esperado no lugar de '{self.lookahead.lexeme}'")

            

    def start(self):
        self.lookahead = globals.scanner.scan()
        return self.program()


    def match(self, tag):
        if self.lookahead.tag == tag:
            self.lookahead = globals.scanner.scan()
            return True
        return False


