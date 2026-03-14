"""
Script de testes para o Lexer e Parser da linguagem Mini-Lang

TESTES DO LEXER:
1. Comentários (//)
2. Números inteiros e reais
3. Strings com escape
4. Tokens básicos
5. Erros lexicos (strings não fechadas, caracteres inválidos)

"""

import sys
import os

# Adicionar o diretório pai ao sys.path para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imports diretos e simples
from Lexer.lexer import Lexer
from constants import *
from error import Error


def print_separator(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_file(filename, test_name, tester_func, verbosity=1):
    """
    Testa um arquivo com uma função de teste customizável
    
    Args:
        filename: nome do arquivo a testar
        test_name: nome do teste para exibição
        tester_func: função que recebe (filename, text) e retorna (resultado, error)
        verbosity: nível de detalhamento (1=completo, 2=erros, 3=silencioso)
    
    Verbosity levels:
    1 - Completo: mostra tudo (separador, código, resultado)
    2 - Apenas erros: mostra separador e erro se houver
    3 - Silencioso: não imprime nada
    """
    
    if verbosity <= 1:
        print_separator(test_name)
    
    filepath = os.path.join(os.path.dirname(__file__), '..', 'exemplos_teste', 'lexer', filename)
    
    if not os.path.exists(filepath):
        if verbosity <= 2:
            print(f"[ERRO] Arquivo nao encontrado: {filepath}")
        return False
    
    if verbosity <= 1:
        print(f"[INFO] Lendo arquivo: {filepath}\n")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        if verbosity <= 1:
            # mostra o conteudo do arquivo
            print("Conteudo do arquivo:")
            print("-" * 60)
            lines = text.split('\n')
            for i, line in enumerate(lines[:15], 1):  # Mostra apenas as 15 primeiras linhas
                print(f"{i:2d}: {line}")
            if len(lines) > 15:
                print(f"... ({len(lines) - 15} linhas omitidas)")
            print("-" * 60)
        
        # Executa a função de teste customizada
        resultado, error = tester_func(filename, text)
        
        if error:
            if verbosity <= 2:
                if verbosity <= 1:
                    print(f"\n[ERRO DETECTADO]:")
                    print(f"\n{error.as_string()}")
                else:
                    print(f"[ERRO] {test_name}")
                    print(f"{error.as_string()}")
            return False
        
        if verbosity == 1:
            # Imprime o resultado
            print(f"\n[OK] Teste passou\n")
            
            # Se for uma lista de tokens, mostra cada um
            if isinstance(resultado, list):
                print(f"Tokens ({len(resultado)} items):\n")
                for i, item in enumerate(resultado, 1):
                    if hasattr(item, 'type') and hasattr(item, 'value'):
                        # É um token - formato: <TIPO, valor>
                        if item.value is not None:
                            print(f"{i:3d}. <{item.type}, {item.value}>")
                        else:
                            print(f"{i:3d}. <{item.type}>")
                    else:
                        print(f"{i:3d}. {item}")
                print()
        
        return True
        
    except Exception as e:
        if verbosity <= 2:
            print(f"[ERRO] Excecao ao processar arquivo: {e}")
            if verbosity <= 1:
                import traceback
                traceback.print_exc()
        return False


def test_lexer(filename, text):
    """
    Función de teste para o Lexer
    Retorna (tokens, error)
    """
    lexer = Lexer(filename, text)
    return lexer.make_tokens()


def main(verbosity=1):
    """
    Executa todos os testes
    
    Verbosity levels:
    1 - Completo: mostra tudo
    2 - Apenas erros
    3 - Silencioso
    """
    print("\n" + "="*60)
    print("TESTES DO LEXER - MINI-LANG")
    print("="*60)
    
    tests = [
        ("test_comentarios.mini", "1. TESTE DE COMENTARIOS (//)", True),
        ("test_numeros.mini", "2. TESTE DE NUMEROS (int e real)", True),
        ("test_strings.mini", "3. TESTE DE STRINGS", True),
        ("test_tokens_basicos.mini", "4. TESTE DE TOKENS BASICOS", True),
        ("test_numeros_edge_cases.mini", "5. TESTE DE NUMEROS - CASOS ESPECIAIS", True),
        ("test_completo_fatorial.mini", "6. TESTE COMPLETO - FATORIAL", True),
        ("test_erros_strings.mini", "7. TESTE DE ERROS - STRINGS NAO FECHADAS", False),
        ("test_erros_caracteres.mini", "8. TESTE DE ERROS - CARACTERES INVALIDOS", False),
    ]
    
    results = []
    for filename, title, should_succeed in tests:
        success = test_file(filename, title, test_lexer, verbosity)
        results.append((title, success, should_succeed))
    
    # Resumo dos testes
    print_separator("RESUMO DOS TESTES")
    
    passed = 0
    failed = 0
    
    for title, success, should_succeed in results:
        if success == should_succeed:
            print(f"[OK] {title}")
            passed += 1
        else:
            print(f"[FAIL] {title}")
            failed += 1
    
    print("\n" + "-"*60)
    print(f"Total: {passed + failed} testes")
    print(f"Passou: {passed}")
    print(f"Falhou: {failed}")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Verbosity pode ser passada como argumento: python test_lexer_mini_lang.py 2
    verbosity = 1
    if len(sys.argv) > 1:
        try:
            verbosity = int(sys.argv[1])
            if verbosity not in [1, 2, 3]:
                print("Verbosity deve ser 1, 2 ou 3")
                sys.exit(1)
        except ValueError:
            print("Argumento inválido. Use: python test_lexer_mini_lang.py [1|2|3]")
            sys.exit(1)
    
    main(verbosity=verbosity)
