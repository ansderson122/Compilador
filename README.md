# Compilador Mini-Lang para Python

Um compilador completo que converte código da linguagem **Mini-Lang** para código **Python** válido e executável.

## Pipeline de Compilação

O compilador executa as seguintes etapas:

```
Mini-Lang Code → Lexer → Parser → Semantic Analyzer → Code Generator → Python Code
```

### 1. **Lexer (Análise Léxica)**
- Lê o código fonte em Mini-Lang
- Identifica tokens (palavras-chave, operadores, identificadores, literais)
- Detecta erros lexicais
- Suporta 29+ tipos de token

### 2. **Parser (Análise Sintática)**
- Recebe os tokens do Lexer
- Constrói a Árvore Sintática Abstrata (AST)
- Valida a estrutura gramatical
- Detecta erros sintáticos
- Implementa Recursive Descent Parsing

### 3. **Semantic Analyzer (Análise Semântica)**
- Verifica tipos de dados com type checking rigoroso
- Valida declarações de variáveis e funções
- Verifica compatibilidade de tipos em operações
- Gerencia escopos com symbol table
- Suporta funções recursivas
- Detecta erros semânticos

### 4. **Code Generator (Gerador de Código)**
- Converte a AST em código Python
- Mapeia construções Mini-Lang para Python equivalentes
- Mantém formatação apropriada

## Estrutura do Projeto

```
ast/
├── Lexer/
│   ├── __init__.py
│   ├── lexer.py
│   ├── token.py
│   └── position.py
├── Parser/
│   ├── __init__.py
│   ├── ast_nodes.py
│   └── paser.py
├── SemanticAnalyzer/
│   ├── __init__.py
│   ├── SemanticAnalyzer.py
│   ├── CodeGenerator.py
│   └── symbol_table.py
├── exemplos_teste/
│   ├── lexer/
│   ├── parser/
│   └── semantic/
├── saidas/  (output - auto-generated)
├── testes/
│   ├── test_lexer_mini_lang.py
│   └── test_parser_mini_lang.py
├── compiler.py  (main entry point)
└── grammer.txt
```

## Requisitos

- Python 3.7+
- Nenhuma dependência externa

## Uso

### Compilar e Salvar Automaticamente

O compilador salva a saída automaticamente em `saidas/<nome_entrada>.py`:

```bash
python compiler.py arquivo.mini
```

**Exemplo:**
```bash
python compiler.py exemplos_teste/semantic/test_var_decl_valido.mini
```

**Saída:**
```
[INFO] Lendo arquivo: exemplos_teste/semantic/test_var_decl_valido.mini

======================================================================
COMPILACAO MINI-LANG -> PYTHON
======================================================================

[1/4] Executando Lexer...
[OK] Lexer concluído - 29 tokens gerados

[2/4] Executando Parser...
[OK] Parser concluído - AST gerada

[3/4] Executando Análise Semântica...
[OK] Análise semântica concluída

[4/4] Gerando código Python...
[OK] Geração de código concluído

[INFO] Salvando código em: saidas\test_var_decl_valido.py
[OK] Arquivo salvo com sucesso
```

### Compilar e Executar

Compile e execute diretamente o código gerado:

```bash
python compiler.py arquivo.mini --exec
```

**Exemplo:**
```bash
python compiler.py exemplos_teste/Factorial.mini --exec
```

**Saída:**
```
[INFO] Lendo arquivo: exemplos_teste/Factorial.mini

======================================================================
COMPILACAO MINI-LANG -> PYTHON
======================================================================

[1/4] Executando Lexer...
[OK] Lexer concluído - 49 tokens gerados

[2/4] Executando Parser...
[OK] Parser concluído - AST gerada

[3/4] Executando Análise Semântica...
[OK] Análise semântica concluída

[4/4] Gerando código Python...
[OK] Geração de código concluído

[INFO] Salvando código em: saidas\Factorial.py
[OK] Arquivo salvo com sucesso

[INFO] Executando código...
----------------------------------------------------------------------
Fatorial de 10:
3628800
----------------------------------------------------------------------
[OK] Execução concluída com sucesso
```

## Exemplos de Código

### 1. Declaração de Variáveis

```mini
var x : int = 10;
var pi : real = 3.14;
var active : bool = true;
var message : string = "Hello World";
```

**Python Gerado:**
```python
x = 10
pi = 3.14
active = True
message = "Hello World"
```

### 2. Operações Aritméticas

```mini
var a : int = 5;
var b : int = 3;
var soma : int = a + b;
var produto : int = a * b;

print "Soma:";
print soma;
print "Produto:";
print produto;
```

**Saída:**
```
Soma:
8
Produto:
15
```

### 3. Função Simples

```mini
def add(a : int, b : int) : int {
    return a + b;
}

def multiply(x : int, y : int) : int {
    return x * y;
}

var result1 : int = add(5, 3);
var result2 : int = multiply(4, 7);

print "Soma:";
print result1;
print "Produto:";
print result2;
```

**Python Gerado:**
```python
def add(a, b):
    return (a + b)

def multiply(x, y):
    return (x * y)

result1 = add(5, 3)
result2 = multiply(4, 7)
print("Soma:")
print(result1)
print("Produto:")
print(result2)
```

### 4. Função Recursiva - Fatorial

```mini
def factorial(n : int) : int {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

var result : int = factorial(10);

print "Fatorial de 10:";
print result;
```

**Python Gerado:**
```python
def factorial(n):
    if (n <= 1):
        return 1

    return (n * factorial((n - 1)))

result = factorial(10)
print("Fatorial de 10:")
print(result)
```

**Saída:**
```
Fatorial de 10:
3628800
```

### 5. Controle de Fluxo - While

```mini
var n : int = 5;
var i : int = 1;
var result : int = 1;

while (i <= n) {
    result = result * i;
    set i = i + 1;
}

print "Fatorial:";
print result;
```

**Python Gerado:**
```python
n = 5
i = 1
result = 1
while (i <= n):
    result = (result * i)
    i = (i + 1)

print("Fatorial:")
print(result)
```

### 6. Controle de Fluxo - If/Else

```mini
var x : int = 10;

if (x > 5) {
    print "x é maior que 5";
}
else {
    print "x é menor ou igual a 5";
}
```

**Python Gerado:**
```python
x = 10
if (x > 5):
    print("x é maior que 5")
else:
    print("x é menor ou igual a 5")
```

## Linguagem Mini-Lang

### Tipos Suportados

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| `int` | Inteiros | `var x : int = 42;` |
| `real` | Números reais | `var pi : real = 3.14;` |
| `bool` | Booleanos | `var flag : bool = true;` |
| `string` | Cadeias de texto | `var msg : string = "Hello";` |
| `void` | Sem retorno | `def func() : void { ... }` |

### Declaração de Variáveis

```mini
var nome : tipo = valor;
```

### Atribuição

```mini
set variavel = novo_valor;
```

### Definição de Funções

```mini
def nome(param1 : tipo1, param2 : tipo2) : tipo_retorno {
    // corpo
    return resultado;
}
```

### Print (Output)

Imprime qualquer expressão:

```mini
print "String literal";
print variavel;
print a + b;
print funcao(args);
```

### Controle de Fluxo

**If/Else:**
```mini
if (condicao) {
    // bloco if
}
else {
    // bloco else
}
```

**While:**
```mini
while (condicao) {
    // bloco repetido
}
```

### Return

```mini
return expressao;
```

### Operadores

| Categoria | Operadores | Exemplo |
|-----------|-----------|---------|
| Aritméticos | `+`, `-`, `*`, `/` | `a + b`, `a * b` |
| Comparação | `==`, `!=`, `<`, `>`, `<=`, `>=` | `x > 5`, `a == b` |
| Lógicos | `and`, `or`, `not` | `x > 0 and y < 10` |
| Unários | `-`, `not` | `-x`, `not flag` |

## Testes

O projeto inclui testes abrangentes:

```bash
# Testes do Lexer
python testes/test_lexer_mini_lang.py

# Testes do Parser
python testes/test_parser_mini_lang.py
```

## Funcionalidades Principais

- ✓ Lexer completo com detecção de erros
- ✓ Parser recursivo descendente com AST
- ✓ Análise semântica com type checking rigoroso
- ✓ Suporte a funções recursivas
- ✓ Geração de código Python válido
- ✓ Symbol table com gerenciamento de escopos
- ✓ Detecção e reportagem de erros com contexto
- ✓ Print com expressões (não apenas strings literais)
- ✓ Compilação automática para `saidas/<nome>.py`
- ✓ Execução direta com `--exec`
- ✓ Sem dependências externas (pure Python)

## Tratamento de Erros

O compilador detecta e reporta erros com contexto preciso:

### Erros Lexicais
```
[ERRO] Erro Lexical:
Caracter invalido: '$'
```

### Erros Sintáticos
```
[ERRO] Erro Sintático:
Sintaxe invalida: Esperado string
File arquivo.mini, line 3
    print variavel;
          ^^^^^^^^^
```

### Erros Semânticos
```
[ERRO] Erro Semântico:
variavel não foi declarada
```

```
[ERRO] Erro Semântico:
Condicao deve ser booleana, obteve int
```

```
[ERRO] Erro Semântico:
Funcao 'add' espera 2 argumentos, mas recebeu 1
```


