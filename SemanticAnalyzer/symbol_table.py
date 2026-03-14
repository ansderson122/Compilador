
class symbol_table:
    def __init__(self):
        self.table = {}

    def __str__(self):
        return str(self.table)
        
    #adiciona um símbolo à tabela, verificando se ele já existe para evitar duplicatas
    def add_symbol(self, symbol, value,type = None):
        if symbol not in self.table:
            self.table[symbol] = {"Value":value,"Type":type}
        else:
            raise Exception(f"{symbol} já foi declarado")

    #verifica se o símbolo existe na tabela
    def verify_symbol(self, symbol):
        return symbol in self.table
    
    #obtém o valor do símbolo se ele existir
    def get_symbol(self, symbol):
        if symbol in self.table:
            return self.table[symbol]
        else:
            raise Exception(f"{symbol} não foi declarado")
    
    #remove o símbolo da tabela se ele existir
    def remove_symbol(self, symbol):
        del self.table[symbol]

class escope: 
    def __init__(self):
        self.table_stack = []
    
    # Permite criar um novo escopo (nova tabela de símbolos) e empilhá-lo na pilha de escopos
    def push_stack(self):
        self.table_stack.append(symbol_table())
    
    # Permite sair do escopo atual, removendo a tabela de símbolos do topo da pilha
    def pop_stack(self):
        if self.table_stack:
            self.table_stack.pop()
        else:
            raise Exception("Escopo falhou: a pilha de tabelas de símbolos está vazia")
    
    # Permite acessar a tabela de símbolos do escopo atual (topo da pilha)
    def current_table(self):
        if self.table_stack:
            return self.table_stack[-1]
        else:
            raise Exception("Escopo falhou: a pilha de tabelas de símbolos está vazia")
    
    # Verifica se um símbolo existe em algum escopo (busca nos escopos pai também)
    def verify_symbol(self, symbol):
        """Busca um símbolo em todos os escopos, começando do topo da pilha"""
        for table in reversed(self.table_stack):
            if table.verify_symbol(symbol):
                return True
        return False
        
    