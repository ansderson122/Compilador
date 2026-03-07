import string

# DIGITS

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS
LETTERS_ACCENTED = 'àáâãäèéêëìíîïòóôõöùúûüçñÀÁÂÃÄÈÉÊËÌÍÎÏÒÓÔÕÖÙÚÛÜÇÑ'  # Letras com acento  
LETTERS_ALL = LETTERS + LETTERS_ACCENTED

# TOKENS

# Literals
TT_INT = 'INT'  # Números inteiros (ex: 5, 42)
TT_REAL = 'REAL'  # Números reais (ex: 3.14, 2.5)
TT_STRING = 'STRING'  # Strings/literais de texto (ex: "texto")
TT_IDENTIFIER = 'IDENTIFIER'  # Identificadores (ex: x, calcular, resultado)
TT_KEYWORD = 'KEYWORD'  # Palavras reservadas (var, def, if, etc)

# Operadores aritméticos
TT_PLUS = 'PLUS'  # Operador de adição (+)
TT_MINUS = 'MINUS'  # Operador de subtração (-)
TT_MUL = 'MUL'  # Operador de multiplicação (*)
TT_DIV = 'DIV'  # Operador de divisão (/)

# Operadores de atribuição
TT_EQ = 'EQ'  # Operador de igualdade (=)
TT_ASSIGN = 'ASSIGN'  # Operador de atribuição (=)

# Parênteses e chaves
TT_LPAREN = 'LPAREN'  # Parêntese esquerdo (
TT_RPAREN = 'RPAREN'  # Parêntese direito )
TT_LBRACE = 'LBRACE'  # Chave esquerda {
TT_RBRACE = 'RBRACE'  # Chave direita }

# Operadores relacionais
TT_EE = 'EE'  # Operador de igualdade (==)
TT_NE = 'NE'  # Operador de não igualdade (!=)
TT_LT = 'LT'  # Operador menor que (<)
TT_GT = 'GT'  # Operador maior que (>)
TT_LTE = 'LTE'  # Operador menor ou igual (<=)
TT_GTE = 'GTE'  # Operador maior ou igual (>=)

# Pontuação
TT_COMMA = 'COMMA'  # Vírgula (,)
TT_COLON = 'COLON'  # Dois-pontos (:)
TT_SEMICOLON = 'SEMICOLON'  # Ponto-e-vírgula (;)

# Controle
TT_EOF = 'EOF'  # Fim do arquivo

KEYWORDS = [
    'var',      # Declaração de variável
    'def',      # Declaração de função
    'if',       # Condicional se
    'else',     # Condicional senão
    'while',    # Loop enquanto
    'return',   # Retorno de função
    'print',    # Impressão na tela
    'set',      # Atribuição de variável
    'int',      # Tipo inteiro
    'real',     # Tipo real/float
    'bool',     # Tipo booleano
    'void',     # Tipo vazio (sem retorno)
    'and',      # Operador lógico E
    'or',       # Operador lógico OU
    'not',      # Operador lógico NÃO
    'true',     # Valor booleano verdadeiro
    'false',    # Valor booleano falso
]