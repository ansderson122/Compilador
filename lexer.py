from enum import Enum
import sys

class TAG(Enum):
    ID = 256
    INTEGER = 257
    FLOATING = 258
    TYPE = 259
    TRUE = 260
    FALSE = 261
    MAIN = 262
    IF = 263
    WHILE = 264
    DO = 265
    OR = 266
    AND = 267
    EQ = 268
    NEQ = 269
    LTE = 270
    GTE = 271

# Definimos uma exceção personalizada para evitar confusão 
# com o "SyntaxError" nativo do Python
class LexerError(Exception):
    def __init__(self, message="Erro na análise léxica"):
        self.message = message
        super().__init__(self.message)

class Token:
    def __init__(self, tag: TAG = 0, lexeme: str = ""):
        self.tag = tag
        self.lexeme = lexeme

class Lexer:
    def __init__(self, file: str, print_tokens: bool = False):
        self._source = file.read()
        self._line = 1 # numero da linha atual
        self._pos = 0 # posicao atual na string do codigo fonte
        self._token_table = {} # tabela de tokens
        self._init_id_table() # inicializa tabela de identificadores
        self._print_tokens = print_tokens

    def get_line(self):
        return self._line        
        
 
    def _init_id_table(self):
        self._id_table = {
            "main": Token(TAG.MAIN.value, "main"),
            "int": Token(TAG.TYPE.value, "int"),
            "float": Token(TAG.TYPE.value, "float"),
            "bool": Token(TAG.TYPE.value, "bool"),
            "true": Token(TAG.TRUE.value, "true"),
            "false": Token(TAG.FALSE.value, "false"),
            "if": Token(TAG.IF.value, "if"),
            "while": Token(TAG.WHILE.value, "while"),
            "do": Token(TAG.DO.value, "do"),
        }

        
    def _get_next_char(self):
        # Implementação do método para obter o próximo caractere do código fonte
        """Simual o cin.get() lendo da string armazenada"""

        if self._pos < len(self._source):
            ch = self._source[self._pos]
            self._pos += 1
            if ch == '\n':
                self._line += 1
            return ch
        return ''
    
    def peek(self):
        # Implementação do método para espiar o próximo caractere sem avançar a posição
        if self._pos < len(self._source):
            return self._source[self._pos]
        return ''
        
    def scan(self):
        # Implementação do método de varredura (scan) do lexer

        # skip whitespace
        while self.peek() and self.peek().isspace():
            self._get_next_char()

        # ignora comentários
        while self.peek() == '/':
            self._get_next_char()
            if self.peek() == '/':
                while self.peek() and self.peek() != '\n':
                    self._get_next_char()
                if self.peek() == '\n':
                    self._get_next_char()
                    self._line += 1
            elif self.peek() == '*':
                self._get_next_char()
                while True:
                    if not self.peek():
                        return Token(0)  # EOF
                    ch = self._get_next_char()
                    if ch == '*' and self.peek() == '/':
                        self._get_next_char()
                        break
            else:
                # Não é um comentário, retorna o token '/'
                self._pos -= 1
                break

        # skip whitespace again
        while self.peek() and self.peek().isspace():
            self._get_next_char()
            
        # Retorna números
        if self.peek() and self.peek().isdigit():
            num_str = ""
            dot_found = False
            while self.peek() and (self.peek().isdigit() or self.peek() == '.'):
                ch = self._get_next_char()
                if ch == '.':
                    if dot_found:
                        break
                    dot_found = True
                num_str += ch
                
            lex = num_str
                
            if dot_found:
                return Token(TAG.FLOATING.value, lex)
            return Token(TAG.INTEGER.value, lex)
        
        # Trata identificadores e palavras reservadas
        if self.peek() and self.peek().isalnum():
            id_str = []
            while self.peek() and self.peek().isalnum():
                id_str.append(self._get_next_char())

            id_str = ''.join(id_str)                
            if id_str in self._id_table:
                # para debugging
                token_found = self._id_table[id_str]
                
                if (self._print_tokens):
                    print(f"<ID, {token_found.name}> ", end='', flush=True)     
                
                return self._id_table[id_str]
            else:
                token = Token(TAG.ID.value, id_str)
                self._token_table[id_str] = token
                return token
            
        
        # operators
        ch = self.peek()
        if ch == '&' and self._pos + 1 < len(self._source) and self._source[self._pos + 1] == '&':
            self._get_next_char()
            self._get_next_char()
            return Token(TAG.AND.value, '&&')
        elif ch == '|' and self._pos + 1 < len(self._source) and self._source[self._pos + 1] == '|':
            self._get_next_char()
            self._get_next_char()
            return Token(TAG.OR.value, '||')
        elif ch == '>' and self._pos + 1 < len(self._source) and self._source[self._pos + 1] == '=':
            self._get_next_char()
            self._get_next_char()
            return Token(TAG.GTE.value, '>=')
        elif ch == '<' and self._pos + 1 < len(self._source) and self._source[self._pos + 1] == '=':
            self._get_next_char()
            self._get_next_char()
            return Token(TAG.LTE.value, '<=')
        elif ch == '=' and self._pos + 1 < len(self._source) and self._source[self._pos + 1] == '=':
            self._get_next_char()
            self._get_next_char()
            return Token(TAG.EQ.value, '==')
        elif ch == '!' and self._pos + 1 < len(self._source) and self._source[self._pos + 1] == '=':
            self._get_next_char()
            self._get_next_char()
            return Token(TAG.NEQ.value, '!=')
        else:
            if ch:
                self._get_next_char()
                return Token(ord(ch), ch)
            else:
                return Token(0)  # EOF
