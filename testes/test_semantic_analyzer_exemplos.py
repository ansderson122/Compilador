"""
Script de testes para o SemanticAnalyzer da linguagem Mini-Lang

TESTES SEMÂNTICOS:
1. Declaração válida de variáveis
2. Operações aritméticas
3. Comparações e operações lógicas
4. Controle de fluxo - IF
5. Controle de fluxo - WHILE
6. Funções simples
7. ERRO: tipo incompatível
8. ERRO: variável não declarada
9. ERRO: condição não-booleana
10. ERRO: argumentos de função incorretos
11. ERRO: tipo de argumento incorreto
"""

import sys
import os

# Adicionar o diretório pai ao sys.path para importar módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imports diretos e simples
from Lexer.lexer import Lexer
from Parser.paser import Parser
from SemanticAnalyzer.SemanticAnalyzer import SemanticAnalyzer
from error import Error


def print_separator(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def test_file(filename, test_name, expect_error=False, verbosity=1):
    """
    Testa um arquivo com análise semântica completa (Lexer -> Parser -> SemanticAnalyzer)
    
    Args:
        filename: nome do arquivo a testar (relativo a exemplos_teste/semantic/)
        test_name: nome do teste para exibição
        expect_error: True se o teste espera um erro semântico
        verbosity: nível de detalhamento (1=completo, 2=erros, 3=silencioso)
    """
    
    if verbosity <= 1:
        print_separator(test_name)
    
    filepath = os.path.join(os.path.dirname(__file__), '..', 'exemplos_teste', 'semantic', filename)
    
    if not os.path.exists(filepath):
        if verbosity <= 2:
            print(f"[ERRO] Arquivo não encontrado: {filepath}")
        return False
    
    if verbosity <= 1:
        print(f"[INFO] Lendo arquivo: {filepath}\n")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        if verbosity <= 1:
            # mostra o conteúdo do arquivo
            print("Conteúdo do arquivo:")
            print("-" * 70)
            lines = text.split('\n')
            for i, line in enumerate(lines, 1):
                print(f"{i:2d}: {line}")
            print("-" * 70)
        
        # ===== LEXER =====
        lexer = Lexer(filename, text)
        tokens, lex_error = lexer.make_tokens()
        
        if lex_error:
            if verbosity <= 2:
                if verbosity <= 1:
                    print(f"\n[ERRO LEXICAL]:")
                    print(f"\n{lex_error.as_string()}")
                else:
                    print(f"[ERRO LEXICAL] {test_name}")
                    print(f"{lex_error.as_string()}")
            return False
        
        if verbosity <= 1:
            print(f"\n[OK] Lexer passou - {len(tokens)} tokens gerados")
        
        # ===== PARSER =====
        parser = Parser(tokens)
        result = parser.parse()
        
        if result.error:
            if verbosity <= 2:
                if verbosity <= 1:
                    print(f"\n[ERRO SINTÁTICO]:")
                    print(f"\n{result.error.as_string()}")
                else:
                    print(f"[ERRO SINTÁTICO] {test_name}")
                    print(f"{result.error.as_string()}")
            return False
        
        ast = result.node
        
        if verbosity <= 1:
            print(f"[OK] Parser passou - AST gerada")
        
        # ===== SEMANTIC ANALYZER =====
        analyzer = SemanticAnalyzer()
        
        try:
            analyzer.analyze(ast)
            
            # Se chegou aqui, não houve erro semântico
            if expect_error:
                if verbosity <= 2:
                    if verbosity <= 1:
                        print(f"\n[FALHA] Esperado erro semântico, mas passou")
                    else:
                        print(f"[FALHA] {test_name} - Esperado erro, mas passou")
                return False
            
            if verbosity <= 1:
                print(f"[OK] Análise semântica passou\n")
            elif verbosity == 2:
                print(f"[OK] {test_name}")
            
            return True
            
        except Exception as sem_error:
            # Houve erro semântico
            if expect_error:
                if verbosity <= 1:
                    print(f"\n[OK] Erro semântico detectado (como esperado):")
                    print(f"\n{str(sem_error)}\n")
                elif verbosity == 2:
                    print(f"[OK] {test_name} - erro detectado como esperado")
                return True
            else:
                if verbosity <= 2:
                    if verbosity <= 1:
                        print(f"\n[ERRO SEMÂNTICO]:")
                        print(f"\n{str(sem_error)}")
                    else:
                        print(f"[ERRO SEMÂNTICO] {test_name}")
                        print(f"{str(sem_error)}")
                return False
        
    except Exception as e:
        if verbosity <= 2:
            print(f"[ERRO] Exceção ao processar arquivo: {e}")
            if verbosity <= 1:
                import traceback
                traceback.print_exc()
        return False


def main(verbosity=1):
    """
    Executa todos os testes semânticos
    
    Verbosity levels:
    1 - Completo: mostra tudo
    2 - Apenas erros
    3 - Silencioso
    """
    print("\n" + "="*70)
    print("TESTES DO SEMANTIC ANALYZER - MINI-LANG")
    print("="*70)
    
    tests = [
        ("test_var_decl_valido.mini", "1. TESTE DE DECLARAÇÃO DE VARIÁVEIS VÁLIDAS", False),
        ("test_operacoes_aritmeticas.mini", "2. TESTE DE OPERAÇÕES ARITMÉTICAS", False),
        ("test_comparacoes_logicas.mini", "3. TESTE DE COMPARAÇÕES E OPERAÇÕES LÓGICAS", False),
        ("test_if_statement.mini", "4. TESTE DE CONTROLE DE FLUXO - IF", False),
        ("test_while_statement.mini", "5. TESTE DE CONTROLE DE FLUXO - WHILE", False),
        ("test_funcoes_simples.mini", "6. TESTE DE FUNÇÕES SIMPLES", False),
        ("test_erro_tipo_incompativel.mini", "7. TESTE DE ERRO - TIPO INCOMPATÍVEL", True),
        ("test_erro_var_undeclared.mini", "8. TESTE DE ERRO - VARIÁVEL NÃO DECLARADA", True),
        ("test_erro_condicao_invalida.mini", "9. TESTE DE ERRO - CONDIÇÃO NÃO-BOOLEANA", True),
        ("test_erro_funcao_args.mini", "10. TESTE DE ERRO - ARGUMENTOS DE FUNÇÃO", True),
        ("test_erro_tipo_argumento.mini", "11. TESTE DE ERRO - TIPO DE ARGUMENTO", True),
    ]
    
    results = []
    
    for filename, test_name, expect_error in tests:
        result = test_file(filename, test_name, expect_error, verbosity)
        results.append((test_name, result))
    
    # ===== RESUMO =====
    print_separator("RESUMO DOS TESTES")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "[✓ OK]" if result else "[✗ FALHA]"
        print(f"{status} {test_name}")
    
    print("\n" + "-"*70)
    print(f"Total: {passed}/{total} testes passaram")
    print("="*70 + "\n")
    
    return passed == total


if __name__ == '__main__':
    import sys
    
    # Detecta o modo verbosity
    verbosity = 1  # padrão: completo
    if len(sys.argv) > 1:
        if sys.argv[1] == '-q':
            verbosity = 2  # quiet: apenas erros
        elif sys.argv[1] == '-qq':
            verbosity = 3  # muito silencioso
    
    success = main(verbosity)
    sys.exit(0 if success else 1)
