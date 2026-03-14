"""
Testes de Integração para o Compilador Mini-Lang
Testa todo o pipeline: Lexer → Parser → SemanticAnalyzer → CodeGenerator
"""

import sys
import os
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from compiler import MiniLangCompiler


def print_separator(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def test_compile_example(filename, expect_error=False, verbosity=1):
    """
    Testa compilação de um exemplo
    
    Args:
        filename: Nome do arquivo (sem caminho)
        expect_error: Se True, espera erro durante compilação
        verbosity: Nível de detalhamento (1=completo, 2=erros)
    
    Returns:
        bool: True se passou, False se falhou
    """
    filepath = os.path.join('exemplos_teste', 'semantic', filename)
    
    if not os.path.exists(filepath):
        print(f"[ERRO] Arquivo não encontrado: {filepath}")
        return False
    
    if verbosity <= 1:
        print_separator(f"TESTE: {filename}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        
        if verbosity <= 1:
            print("Código Mini-Lang:")
            print("-"*70)
            lines = code.split('\n')
            for i, line in enumerate(lines, 1):
                print(f"{i:2d}: {line}")
            print("-"*70)
        
        compiler = MiniLangCompiler(filename, code)
        python_code, error = compiler.compile()
        
        if error:
            if expect_error:
                if verbosity <= 1:
                    print(f"\n[OK] Erro esperado detectado")
                return True
            else:
                if verbosity <= 2:
                    print(f"\n[ERRO] Compilação falhou (inesperado):\n{error}")
                return False
        
        # Compilação bem-sucedida
        if expect_error:
            if verbosity <= 2:
                print(f"\n[ERRO] Compilação bem-sucedida, mas esperava erro")
            return False
        
        if verbosity <= 1:
            print(f"\nCódigo Python gerado:")
            print("-"*70)
            print(python_code)
            print("-"*70)
            print(f"\n[✓] Compilação bem-sucedida")
        
        return True
        
    except Exception as e:
        if verbosity <= 2:
            print(f"[ERRO] Exceção: {e}")
            import traceback
            traceback.print_exc()
        return False


def main(verbosity=1):
    """
    Executa testes de integração
    
    Args:
        verbosity: Nível de detalhamento (1=completo, 2=erros, 3=silencioso)
    """
    print("\n" + "="*70)
    print("TESTES DE INTEGRAÇÃO - COMPILADOR MINI-LANG")
    print("="*70)
    
    tests = [
        ("test_var_decl_valido.mini", False),
        ("test_operacoes_aritmeticas.mini", False),
        ("test_comparacoes_logicas.mini", False),
        ("test_if_statement.mini", False),
        ("test_while_statement.mini", False),
        ("test_funcoes_simples.mini", False),
        ("test_erro_tipo_incompativel.mini", True),
        ("test_erro_var_undeclared.mini", True),
        ("test_erro_condicao_invalida.mini", True),
    ]
    
    results = []
    
    for filename, expect_error in tests:
        result = test_compile_example(filename, expect_error, verbosity)
        results.append((filename, result))
    
    # ===== RESUMO =====
    print_separator("RESUMO DOS TESTES DE INTEGRAÇÃO")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for filename, result in results:
        status = "[OK]" if result else "[FALHA]"
        print(f"{status} {filename}")
    
    print("\n" + "-"*70)
    print(f"Total: {passed}/{total} testes passaram")
    print("="*70 + "\n")
    
    return passed == total


if __name__ == '__main__':
    verbosity = 1
    if len(sys.argv) > 1:
        if sys.argv[1] == '-q':
            verbosity = 2
        elif sys.argv[1] == '-qq':
            verbosity = 3
    
    success = main(verbosity)
    sys.exit(0 if success else 1)
