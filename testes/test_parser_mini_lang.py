"""
Script de testes para o Parser da linguagem Mini-Lang

Os testes do Lexer estão em: test_lexer_mini_lang.py

TESTES DO PARSER:
1. Declaração de variável
2. Operações aritméticas
3. Funções
4. Controle de fluxo (if/while)
5. Programas completos
6. Erros de sintaxe
"""

import sys
import os

# Adicionar os caminhos ao sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Lexer'))
sys.path.insert(0, os.path.dirname(__file__) + '/..')

from Lexer.lexer import Lexer
from Parser.paser import Parser
from constants import *
from error import Error


def print_separator(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_file_parser(filename, test_name, verbosity=1):
    """
    Testa um arquivo com o parser
    
    Args:
        filename: nome do arquivo a testar
        test_name: nome do teste para exibição
        verbosity: nível de detalhamento (1=completo, 2=erros, 3=silencioso)
    
    Verbosity levels:
    1 - Completo: mostra tudo (separador, código, resultado)
    2 - Apenas erros: mostra separador e erro se houver
    3 - Silencioso: não imprime nada
    """
    
    if verbosity <= 1:
        print_separator(test_name)
    
    filepath = os.path.join(os.path.dirname(__file__), '..', 'exemplos_teste', 'parser', filename)
    
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
            for i, line in enumerate(lines[:20], 1):  # Mostra apenas as 20 primeiras linhas
                print(f"{i:2d}: {line}")
            if len(lines) > 20:
                print(f"... ({len(lines) - 20} linhas omitidas)")
            print("-" * 60)
        
        # Executa o lexer primeiro
        lexer = Lexer(filename, text)
        tokens, error = lexer.make_tokens()
        
        if error:
            if verbosity <= 2:
                if verbosity <= 1:
                    print(f"\n[ERRO LEXER]:")
                    print(f"\n{error.as_string()}")
                else:
                    print(f"[ERRO LEXER] {test_name}")
                    print(f"{error.as_string()}")
            return False
        
        # Executa o parser
        parser = Parser(tokens)
        ast = parser.parse()
        
        if ast.error:
            if verbosity <= 2:
                if verbosity <= 1:
                    print(f"\n[ERRO PARSER]:")
                    print(f"\n{ast.error.as_string()}")
                else:
                    print(f"[ERRO PARSER] {test_name}")
                    print(f"{ast.error.as_string()}")
            return False
        
        if verbosity == 1:
            # Imprime o resultado
            print(f"\n[OK] Teste passou\n")
            
            # Mostra a AST
            if ast.node:
                print(f"AST gerada:\n")
                print(f"{ast.node}\n")
        
        return True
        
    except Exception as e:
        if verbosity <= 2:
            print(f"[ERRO] Excecao ao processar arquivo: {e}")
            if verbosity <= 1:
                import traceback
                traceback.print_exc()
        return False


def main(verbosity=1):
    """
    Executa todos os testes do Parser
    
    Verbosity levels:
    1 - Completo: mostra tudo
    2 - Apenas erros
    3 - Silencioso
    """
    print("\n" + "="*60)
    print("TESTES DO PARSER - MINI-LANG")
    print("="*60)
    
    tests = [
        ("test_var_decl.mini", "1. TESTE - DECLARACAO DE VARIAVEL", True),
        ("test_aritmetica.mini", "2. TESTE - EXPRESSOES ARITMETICAS", True),
        ("test_funcao_simples.mini", "3. TESTE - FUNCAO SIMPLES", True),
        ("test_if_while.mini", "4. TESTE - IF E WHILE", True),
        ("test_fatorial_completo.mini", "5. TESTE COMPLETO - FATORIAL", True),
        ("test_funcoes_multiplas.mini", "6. TESTE - MULTIPLAS FUNCOES", True),
        ("test_erro_sintaxe_1.mini", "7. TESTE - ERRO SINTAXICO 1", False),
        ("test_erro_sintaxe_2.mini", "8. TESTE - ERRO SINTAXICO 2", False),
    ]
    
    results = []
    for filename, title, should_succeed in tests:
        success = test_file_parser(filename, title, verbosity)
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
    # Verbosity pode ser passada como argumento: python test_parser_mini_lang.py 2
    verbosity = 1
    if len(sys.argv) > 1:
        try:
            verbosity = int(sys.argv[1])
            if verbosity not in [1, 2, 3]:
                print("Verbosity deve ser 1, 2 ou 3")
                sys.exit(1)
        except ValueError:
            print("Argumento inválido. Use: python test_parser_mini_lang.py [1|2|3]")
            sys.exit(1)
    
    main(verbosity=verbosity)
