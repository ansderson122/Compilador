import sys
from lexer import Lexer
from parser import Parser
from error import SyntaxError
import globals

if __name__ == "__main__":
    # 1. Verifica se o usuário passou o nome do arquivo
    if len(sys.argv) < 2:
        print("Uso: python parser.py <arquivo_fonte>")
        sys.exit(1)

    if len(sys.argv) == 2:
        try:
            with open(sys.argv[1], 'r') as file:
                globals.scanner = Lexer(file)
                ast = Parser().start()
                ast.Gen()
        except SyntaxError as err:
            err.what()          
        except FileNotFoundError:
            print(f"Erro: O arquivo '{sys.argv[1]}' não foi encontrado.")

    print() # quebra de linha final