
# Esse arquivo contém as classes de erros que o interpretador pode encontrar durante a execução do código.
# Cada classe de erro herda da classe base 'Error' e tem um método 'as_string' para formatar a mensagem de erro de forma legível, incluindo a posição do erro no código-fonte e uma indicação visual do local do erro.

class Error:
    """Classe base para erros encontrados durante a análise léxica, sintática e execução do código-fonte"""
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def string_with_arrows(self, text, pos_start, pos_end):
        """Retorna uma string com setas indicando a posição do erro no código-fonte
        Args:
            text (str): O código-fonte completo
            pos_start (Position): A posição inicial do erro
            pos_end (Position): A posição final do erro
        Returns:            
          str: Uma string formatada com setas indicando a posição do erro
        
        """
        result = ''

        
        idx_start = max(text.rfind('\n', 0, pos_start.idx), 0)
        idx_end = text.find('\n', idx_start + 1)
        if idx_end < 0: idx_end = len(text)
        

        line_count = pos_end.ln - pos_start.ln + 1
        for i in range(line_count):
            
            line = text[idx_start:idx_end]
            col_start = pos_start.col if i == 0 else 0
            col_end = pos_end.col if i == line_count - 1 else len(line) - 1

            result += line + '\n'
            result += ' ' * col_start + '^' * (col_end - col_start)


            idx_start = idx_end
            idx_end = text.find('\n', idx_start + 1)
            if idx_end < 0: idx_end = len(text)

        return result.replace('\t', '')

    def as_string(self):
        """Retorna a mensagem de erro formatada como string
        Returns:
            str: A mensagem de erro formatada, incluindo o nome do erro, detalhes e a posição do erro no código-fonte
        """
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        result += '\n\n' + \
            self.string_with_arrows(self.pos_start.ftxt,
                                   self.pos_start, self.pos_end)
        return result


class IllegalCharError(Error):
    """Erro para caracteres inválidos encontrados durante a análise léxica"""
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Caractere invalido', details)


class ExpectedCharError(Error):
    """Erro para caracteres esperados mas não encontrados"""
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Caractere esperado', details)


class InvalidSyntaxError(Error):
    """Erro para sintaxe inválida encontrada durante a análise sintática"""
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Sintaxe invalida', details)