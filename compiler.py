"""
Compilador Mini-Lang para Python
Integra: Lexer → Parser → SemanticAnalyzer → CodeGenerator
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from Lexer.lexer import Lexer
from Parser.paser import Parser
from SemanticAnalyzer.SemanticAnalyzer import SemanticAnalyzer
from SemanticAnalyzer.CodeGenerator import CodeGenerator


class MiniLangCompiler:
    """
    Compilador completo da linguagem Mini-Lang
    Converte código Mini-Lang para código Python
    """
    
    def __init__(self, filename, code):
        """
        Inicializa o compilador
        
        Args:
            filename: Nome do arquivo sendo compilado
            code: Código fonte em Mini-Lang
        """
        self.filename = filename
        self.code = code
        self.error = None
    
    def compile(self):
        """
        Executa o processo completo de compilação
        
        Returns:
            tuple: (código_python, erro) ou (None, erro) se falhar
        """
        # ===== LEXER =====
        print(f"[1/4] Executando Lexer...")
        lexer = Lexer(self.filename, self.code)
        tokens, lex_error = lexer.make_tokens()
        
        if lex_error:
            print(f"[ERRO] Erro Lexical:\n{lex_error.as_string()}")
            self.error = lex_error
            return None, lex_error
        
        print(f"[OK] Lexer concluído - {len(tokens)} tokens gerados")
        
        # ===== PARSER =====
        print(f"\n[2/4] Executando Parser...")
        parser = Parser(tokens)
        result = parser.parse()
        
        if result.error:
            print(f"[ERRO] Erro Sintático:\n{result.error.as_string()}")
            self.error = result.error
            return None, result.error
        
        print(f"[OK] Parser concluído - AST gerada")
        ast = result.node
        
        # ===== SEMANTIC ANALYZER =====
        print(f"\n[3/4] Executando Análise Semântica...")
        analyzer = SemanticAnalyzer()
        
        try:
            analyzer.analyze(ast)
            print(f"[OK] Análise semântica concluída")
        except Exception as sem_error:
            print(f"[ERRO] Erro Semântico:\n{str(sem_error)}")
            self.error = sem_error
            return None, sem_error
        
        # ===== CODE GENERATOR =====
        print(f"[4/4] Gerando código Python...")
        generator = CodeGenerator()
        
        try:
            python_code = generator.generate(ast)
            print(f"[OK] Geração de código concluída")
            return python_code, None
        except Exception as gen_error:
            print(f"[ERRO] Erro ao gerar código:\n{str(gen_error)}")
            self.error = gen_error
            return None, gen_error
    
    def compile_and_save(self, output_filename=None):
        """
        Compila e salva o código Python em arquivo
        
        Args:
            output_filename: Nome do arquivo de saída (padrão: saidas/<nome_entrada>.py)
        
        Returns:
            tuple: (sucesso, nome_arquivo) se sucesso, (False, None) se erro
        """
        python_code, error = self.compile()
        
        if error:
            return False, None
        
        # Se não foi especificado, gera automaticamente
        if output_filename is None:
            # Cria pasta saidas se não existir
            output_dir = 'saidas'
            os.makedirs(output_dir, exist_ok=True)
            
            # Extrai nome do arquivo sem caminho e muda extensão para .py
            basename = os.path.basename(self.filename)
            base_without_ext = os.path.splitext(basename)[0]
            output_filename = os.path.join(output_dir, f"{base_without_ext}.py")
        
        print(f"[INFO] Salvando código em: {output_filename}")
        
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(python_code)
            
            print(f"[OK] Arquivo salvo com sucesso")
            return True, output_filename
        except Exception as e:
            print(f"[ERRO] Erro ao salvar arquivo: {e}")
            return False, None
    
    def compile_and_execute(self):
        """
        Compila, salva e executa o código Python
        
        Returns:
            int: Código de saída (0 se sucesso)
        """
        # Compila uma única vez
        python_code, error = self.compile()
        
        if error:
            return 1 
        
        # Salva o arquivo
        output_dir = 'saidas'
        os.makedirs(output_dir, exist_ok=True)
        
        basename = os.path.basename(self.filename)
        base_without_ext = os.path.splitext(basename)[0]
        output_filename = os.path.join(output_dir, f"{base_without_ext}.py")
        
        print(f"[INFO] Salvando código em: {output_filename}")
        
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(python_code)
            print(f"[OK] Arquivo salvo com sucesso")
        except Exception as e:
            print(f"[ERRO] Erro ao salvar arquivo: {e}")
            return 1
        
        # Executa o código compilado
        print(f"\n[INFO] Executando código...")
        print('-'*70)
        
        try:
            # Cria um namespace global para a execução
            namespace = {}
            exec(python_code, namespace)
            print('-'*70)
            print(f"[OK] Execução concluída com sucesso")
            return 0
        except Exception as e:
            print('-'*70)
            print(f"[ERRO] Erro durante execução:\n{str(e)}")
            import traceback
            traceback.print_exc()
            return 1


def main():
    """Função principal"""
    if len(sys.argv) < 2:
        print("Uso: python compiler.py <arquivo.mini> [--exec]")
        print()
        print("Opcoes:")
        print("  --exec  Executa o código gerado após compilar")
        print()
        print("Saída padrão: saidas/<nome_entrada>.py")
        sys.exit(1)
    
    input_file = sys.argv[1]
    execute = '--exec' in sys.argv
    
    # Verifica se arquivo existe
    if not os.path.exists(input_file):
        print(f"[ERRO] Arquivo não encontrado: {input_file}")
        sys.exit(1)
    
    # Lê o arquivo
    print(f"[INFO] Lendo arquivo: {input_file}\n")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        print(f"[ERRO] Falha ao ler arquivo: {e}")
        sys.exit(1)
    
    # Compila
    print("="*70)
    print("COMPILACAO MINI-LANG -> PYTHON")
    print("="*70)
    print()
    
    compiler = MiniLangCompiler(input_file, code)
    
    if execute:
        exit_code = compiler.compile_and_execute()
        sys.exit(exit_code)
    else:
        success, output_filename = compiler.compile_and_save()
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
