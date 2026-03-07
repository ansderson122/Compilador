class Symbol:
    """
    Estrutura para salvar o nome de uma variável e o tipo
    """
    def __init__(self, var, type):
        self.var = var
        self.type = type
    
    def __repr__(self):
        return f"Symbol(var='{self.var}', type='{self.type}')"
    
class SymTable:
    def __init__(self, prev=None):
        """
        Construtor do SymTable.
        Se prev for None, essa é uma tabela global (escopo mais externo)
        Se 'prev' for passado, é uma nova tabela aninhada a ser criada 
        dentro do escopo de 'prev'
        """
        self.table = {} # tabela inicia vazia
        self.prev = prev

    def insert(self, s: str, symb: Symbol):
        """
        Função para inseir um símbolo na tabela atual
        Retorna True se inseriu com sucesso, False se já
         existia a entrada na tabela
        
        :param self: Descrição
        :param s: Descrição
        :type s: str
        :param symb: Descrição
        :type symb: symbol
        :rtype: bool
        """
        if s in self.table:
            return False
        
        self.table[s] = symb
        return True
    
    def find(self, s):
        """
        Docstring para find
        
        :param self: Descrição
        :param s: Descrição
        :return: Descrição
        :rtype: Any | None
        """
        #começa a busca na tabela atual
        current_scope = self

        # percorre as referÊncias para prev
        while current_scope is not None:
            if s in current_scope.table:
                return current_scope.table[s]
            
            # sobe para o escopo anterior
            current_scope = current_scope.prev

        return None
    

if __name__ == "__main__":
    
    print("Testanto a classe SymTable")

    # 1. Criando escopo global
    global_scope = SymTable()
    print("Escopo Global Criado!")

    # inserir uma variável global 'x' (int)
    sym1 = Symbol("x", "int")
    global_scope.insert("x", sym1)
    print(f"Inserido no escopo Global: x -> {global_scope.find('x')}")


    # 2. Criar escopo local (ex: dentro de uma função)
    # Passamos o global_scope como 'prev''
    local_scope = SymTable(prev=global_scope)
    print("Escopo local criado dentro do escopo global!")

    # inserir uma variável local 'y' (float)
    sym2 = Symbol("y", "float")
    local_scope.insert("y", sym2)

    # 3. Testes de Busca (Lookup)
    print(f"Buscando 'y' no local: {local_scope.find('y')}") # Deve achar no local
    print(f"Buscando 'x' no local: {local_scope.find('x')}") # Deve achar no global (via prev)

    print("====================================================")

    # 4. Sombreamento (Shadowing)
    print("Inserindo 'x' no escopo local (Shadowing)...")
    sym3 = Symbol("x", "char") # Novo x, agora char
    local_scope.insert("x", sym3)


    print(f"Buscando 'x' no local:  {local_scope.find('x')}")  # Deve ser char (local)
    print(f"Buscando 'x' no global: {global_scope.find('x')}") # Deve ser int (original)