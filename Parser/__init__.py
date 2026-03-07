"""
Pacote Parser - Análise Sintática para Mini-Lang

Este pacote contém os módulos necessários para análise sintática
e geração de Árvore de Sintaxe Abstrata (AST) para a linguagem Mini-Lang.

Módulos:
- paser.py: Classe Parser (análise recursiva descendente)
- ast_nodes.py: Classes de nós da AST (Abstract Syntax Tree)
"""

from .paser import Parser, ParseResult
from .ast_nodes import (
    # Nós de programa
    ProgramNode,
    BlockNode,
    
    # Nós de literais
    NumberNode,
    StringNode,
    BooleanNode,
    
    # Nós de identificadores
    IdentifierNode,
    
    # Nós de expressões
    BinaryOpNode,
    UnaryOpNode,
    
    # Nós de declarações
    VariableDeclNode,
    AssignmentNode,
    PrintNode,
    
    # Nós de controle
    ReturnNode,
    IfNode,
    WhileNode,
    
    # Nós de funções
    FunctionDeclNode,
    FunctionCallNode,
)


__all__ = [
    # Parser
    'Parser',
    'ParseResult',
    
    # AST Nodes - Programa
    'ProgramNode',
    'BlockNode',
    
    # AST Nodes - Literais
    'NumberNode',
    'StringNode',
    'BooleanNode',
    
    # AST Nodes - Identificadores
    'IdentifierNode',
    
    # AST Nodes - Expressões
    'BinaryOpNode',
    'UnaryOpNode',
    
    # AST Nodes - Declarações
    'VariableDeclNode',
    'AssignmentNode',
    'PrintNode',
    
    # AST Nodes - Controle
    'ReturnNode',
    'IfNode',
    'WhileNode',
    
    # AST Nodes - Funções
    'FunctionDeclNode',
    'FunctionCallNode',
]
