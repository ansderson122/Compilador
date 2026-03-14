from Parser.ast_nodes import ProgramNode


class CodeGenerator:
    """
    Converte uma AST (já analisada semanticamente) em código Python.
    
    O SemanticAnalyzer valida a AST, e o CodeGenerator gera o código Python
    correspondente usando os métodos to_python() dos nós.
    """
    
    def __init__(self):
        pass
    
    def generate(self, ast_node):
        """
        Gera código Python a partir da AST
        
        Args:
            ast_node: O nó raiz da AST (geralmente ProgramNode)
        
        Returns:
            string: Código Python gerado
        """
        if ast_node is None:
            return ""
        
        # Chama o método to_python() do nó
        code = ast_node.to_python(0)
        return code
    
    def generate_to_file(self, ast_node, output_filename):
        """
        Gera código Python e salva em arquivo
        
        Args:
            ast_node: O nó raiz da AST
            output_filename: Nome do arquivo de saída
        
        Returns:
            bool: True se sucesso, False se erro
        """
        try:
            code = self.generate(ast_node)
            
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(code)
            
            return True
        except Exception as e:
            print(f"[ERRO] Falha ao gerar arquivo: {e}")
            return False
