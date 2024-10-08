import re

# Lista de tokens com seus respectivos padrões regex
tokens = [
    ("PROGRAM", r'programa'),
    ("SEMICOLON", r';'),
    ("DOT", r'\.'),
    ("LBRACE", r'\{'),
    ("RBRACE", r'\}'),
    ("PROCEDURE", r'procedimento'),
    ("FUNCTION", r'funcao'),
    ("LPAREN", r'\('),
    ("RPAREN", r'\)'),
    ("COMMA", r','),
    ("ASSIGN", r'='),
    ("IF", r'if'),
    ("FIM_IF", r'fim_if'),
    ("ELSE", r'else'),
    ("FIM_ELSE", r'fim_else'),
    ("WHILE", r'while'),
    ("FIM_WHILE", r'fim_while'),
    ("RETURN", r'retorno'),
    ("CONTINUE", r'continue'),
    ("BREAK", r'break'),
    ("PRINT", r'imprimir'),
    ("INT", r'int'),
    ("BOOL", r'bool'),
    ("TRUE", r'True'),
    ("FALSE", r'False'),
    ("EQ", r'=='),
    ("NEQ", r'!='),
    ("GT", r'>'),
    ("LT", r'<'),
    ("GTE", r'>='),
    ("LTE", r'<='),
    ("PLUS", r'\+'),
    ("MINUS", r'-'),
    ("MULT", r'\*'),
    ("DIV", r'/'),
    ("MOD", r'%'),
    ("STRING", r'"[^"]*"'),  
    ("IDENTIFIER", r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ("NUMBER", r'\d+'),
    ("WHITESPACE", r'\s+'),
]

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = self.tokenize(code)
    
    def tokenize(self, code):
        token_list = []
        while self.position < len(code):
            match = None
            for token_expr in tokens:
                pattern, regex = token_expr
                regex = re.compile(regex)
                match = regex.match(code, self.position)
                if match:
                    text = match.group(0)
                    if pattern != "WHITESPACE":  # Ignora espaços em branco
                        token_list.append((pattern, text, self.line, self.column))
                    self.update_position(text)
                    break
            if not match:
                print(f"Erro no caractere: {code[self.position]} na posição {self.position}")
                raise SyntaxError(f"Illegal character: {code[self.position]} at line {self.line}, column {self.column}")
            else:
                self.position = match.end(0)
        return token_list

    def update_position(self, text):
        lines = text.split('\n')
        if len(lines) > 1:
            self.line += len(lines) - 1
            self.column = len(lines[-1]) + 1
        else:
            self.column += len(text)

    def next_token(self):
        if self.tokens:
            return self.tokens.pop(0)
        else:
            return None

    def get_tokens(self):
        return self.tokens

if __name__ == "__main__":
    test_files = [
        'tests/atribuicao.txt',
        'tests/chamada_funcao.txt',
        'tests/chamada_procedimento.txt',
        'tests/condicional.txt',
        'tests/declaracao_funcao.txt',
        'tests/declaracao_procedimento.txt',
        'tests/declaracao_variavel.txt',
        'tests/enquanto.txt',
        'tests/escrita.txt',
        'tests/operacoes.txt'
    ]

    for test_file in test_files:
        with open(test_file, 'r') as file:
            code = file.read()
            lexer = Lexer(code)
            
            print(f"\nTokens para {test_file}:")
            for token in lexer.get_tokens():
                print(token)
