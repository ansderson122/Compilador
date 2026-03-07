import sys
sys.path.insert(0, 'Lexer')
from lexer import Lexer

# Teste simples com comentário
code = '''// Este é um comentário simples
var x : int = 5;'''

lexer = Lexer('test.mini', code)
tokens, error = lexer.make_tokens()

if error:
    print('❌ ERRO:')
    print(error.as_string())
else:
    print('✅ Tokens:')
    for token in tokens:
        print(f'  {token.type}: {token.value if token.value else ""}')
