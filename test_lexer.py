import sys
from lexer import Lexer, TAG

if __name__ == "__main__":

    # 1. Verifica se o usuário passou o nome do arquivo
    # if len(sys.argv) < 2:
    #     print("Uso: python parser.py <arquivo_fonte>")
    #     sys.exit(1)

    # nome_arquivo = sys.argv[1]
    lexer = Lexer('testes/teste1.cpp')
    
    t = lexer.scan()
    while t.tag != '\0':
        
        if t.tag == TAG.ID:
            print(f"Token: ID, Lexema: {t.lexeme}")
        elif t.tag == TAG.INTEGER:
            print(f"Token: INTEGER, Lexema: {t.lexeme}")
        elif t.tag == TAG.REAL:
            print(f"Token: REAL, Lexema: {t.lexeme}")
        elif t.tag == TAG.TRUE:
            print(f"Token: TRUE, Lexema: {t.lexeme}")
        elif t.tag == TAG.FALSE:
            print(f"Token: FALSE, Lexema: {t.lexeme}")
        elif t.tag == TAG.MAIN:
            print(f"Token: MAIN, Lexema: {t.lexeme}")
        elif t.tag == TAG.IF:
            print(f"Token: IF, Lexema: {t.lexeme}")
        elif t.tag == TAG.WHILE:
            print(f"Token: WHILE, Lexema: {t.lexeme}")
        elif t.tag == TAG.DO:
            print(f"Token: DO, Lexema: {t.lexeme}")
        elif t.tag == TAG.OR:
            print(f"Token: OR, Lexema: {t.lexeme}")
        elif t.tag == TAG.AND:
            print(f"Token: AND, Lexema: {t.lexeme}")
        elif t.tag == TAG.EQ:
            print(f"Token: EQ, Lexema: {t.lexeme}")
        elif t.tag == TAG.NEQ:
            print(f"Token: NEQ, Lexema: {t.lexeme}")
        elif t.tag == TAG.LET:
            print(f"Token: LET, Lexema: {t.lexeme}")
        elif t.tag == TAG.GTE:
            print(f"Token: GTE, Lexema: {t.lexeme}")
        else:
            print(f"Token: {t.tag}, Lexema: {t.lexeme}")

        # Process token t here
        t = lexer.scan()