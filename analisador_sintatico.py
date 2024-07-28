from analisador_lexico import Lexer

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next_token()

    def eat(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            self.current_token = self.lexer.next_token()
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token}")

    def programa(self):
        self.eat("PROGRAM")
        self.eat("IDENTIFIER")
        self.eat("SEMICOLON")
        self.bloco()
        if self.current_token:
            raise SyntaxError(f"Unexpected token at the end of program: {self.current_token}")

    def bloco(self):
        while self.current_token and self.current_token[0] in {
            "PROCEDURE", "FUNCTION", "INT", "BOOL", "IDENTIFIER",
            "IF", "WHILE", "RETURN", "CONTINUE", "BREAK", "PRINT"
        }:
            self.comando()

    def comando(self):
        if self.current_token[0] in {"INT", "BOOL"}:
            self.declaracao_variavel()
        elif self.current_token[0] == "PROCEDURE":
            self.declaracao_procedimento()
        elif self.current_token[0] == "FUNCTION":
            self.declaracao_funcao()
        elif self.current_token[0] == "IDENTIFIER":
            self.atribuicao_ou_chamada()
        elif self.current_token[0] == "IF":
            self.declaracao_if()
        elif self.current_token[0] == "WHILE":
            self.declaracao_while()
        elif self.current_token[0] == "RETURN":
            self.declaracao_retorno()
        elif self.current_token[0] in {"CONTINUE", "BREAK"}:
            self.incondicional()
        elif self.current_token[0] == "PRINT":
            self.declaracao_imprimir()
        else:
            raise SyntaxError(f"Unexpected token in comando: {self.current_token}")

    def atribuicao_ou_chamada(self):
        print(f"Processing token: {self.current_token}")
        identifier = self.current_token
        self.eat("IDENTIFIER")
        
        if self.current_token and self.current_token[0] == "ASSIGN":
            print(f"Assignment detected for identifier: {identifier}")
            self.eat("ASSIGN")
            self.expressao()
            self.eat("SEMICOLON")
        elif self.current_token and self.current_token[0] == "LPAREN":
            print(f"Function call detected for identifier: {identifier}")
            self.eat("LPAREN")
            self.argumentos()
            self.eat("RPAREN")
            self.eat("SEMICOLON")
        else:
            raise SyntaxError(f"Expected ASSIGN or LPAREN after identifier, got {self.current_token}")

    def argumentos(self):
        if self.current_token and self.current_token[0] in {"IDENTIFIER", "NUMBER"}:
            self.expressao()
            while self.current_token and self.current_token[0] == "COMMA":
                self.eat("COMMA")
                self.expressao()
        elif self.current_token and self.current_token[0] == "RPAREN":
            # No arguments, just closing parenthesis
            return
        else:
            raise SyntaxError(f"Expected IDENTIFIER, NUMBER, or RPAREN, got {self.current_token}")

    def declaracao_variavel(self):
        self.eat(self.current_token[0])  # INT ou BOOL
        self.eat("IDENTIFIER")
        self.eat("SEMICOLON")

    def declaracao_procedimento(self):
        self.eat("PROCEDURE")
        self.eat("IDENTIFIER")
        self.eat("LPAREN")
        if self.current_token and self.current_token[0] in {"INT", "BOOL"}:
            self.parametro()
            while self.current_token and self.current_token[0] == "COMMA":
                self.eat("COMMA")
                self.parametro()
        self.eat("RPAREN")
        self.eat("LBRACE")
        self.bloco()
        self.eat("RBRACE")

    def declaracao_funcao(self):
        self.eat("FUNCTION")
        self.eat("INT")  # Tipo de retorno da função, pode ser alterado conforme necessário
        self.eat("IDENTIFIER")
        self.eat("LPAREN")
        if self.current_token and self.current_token[0] in {"INT", "BOOL"}:
            self.parametro()
            while self.current_token and self.current_token[0] == "COMMA":
                self.eat("COMMA")
                self.parametro()
        self.eat("RPAREN")
        self.eat("LBRACE")
        self.bloco()
        if self.current_token and self.current_token[0] == "RETURN":
            self.declaracao_retorno()
        self.eat("RBRACE")

    def declaracao_if(self):
        self.eat("IF")
        self.eat("LPAREN")
        self.expressao() 
        self.eat("RPAREN")
        self.eat("LBRACE")
        self.bloco()  
        self.eat("RBRACE")
        self.eat("IDENTIFIER") 
        
        # Processa a parte else opcional
        self.declaracao_else()

    def declaracao_else(self):
        if self.current_token and self.current_token[0] == "ELSE":
            self.eat("ELSE")
            self.eat("LBRACE")
            self.bloco()  
            self.eat("RBRACE")
            self.eat("IDENTIFIER")  # Consome o "fim_else"
        elif self.current_token and self.current_token[0] == "IDENTIFIER" and self.current_token[1] == "fim_else":
            self.eat("IDENTIFIER")  


    def declaracao_while(self):
        self.eat("WHILE")
        self.eat("LPAREN")
        self.expressao()
        self.eat("RPAREN")
        self.eat("LBRACE")
        self.bloco()
        self.eat("RBRACE")
        # Espera o token fim_while
        if not self.current_token:
            raise SyntaxError("Expected 'fim_while', but reached end of file")
        
        if self.current_token[0] != "IDENTIFIER" or self.current_token[1] != "fim_while":
            raise SyntaxError(f"Expected 'fim_while', got {self.current_token}")
        
        self.eat("IDENTIFIER")  # Consome o "fim_while"

    def declaracao_retorno(self):
        self.eat("RETURN")
        self.expressao()
        self.eat("SEMICOLON")

    def incondicional(self):
        self.eat(self.current_token[0])  # CONTINUE ou BREAK
        self.eat("SEMICOLON")

    def declaracao_imprimir(self):
            self.eat("PRINT")
            self.eat("LPAREN")
            if self.current_token[0] == "STRING":
                self.eat("STRING")
            else:
                self.expressao()
            self.eat("RPAREN")
            self.eat("SEMICOLON")

    def parametro(self):
        self.eat(self.current_token[0])  # INT ou BOOL
        self.eat("IDENTIFIER")

    def expressao(self):
        self.expressao_simples()
        if self.current_token and self.current_token[0] in {"EQ", "NEQ", "GT", "LT", "GTE", "LTE"}:
            self.eat(self.current_token[0])
            self.expressao_simples()

    def expressao_simples(self):
        if self.current_token and self.current_token[0] in {"PLUS", "MINUS"}:
            self.eat(self.current_token[0])
        self.termo()
        while self.current_token and self.current_token[0] in {"PLUS", "MINUS"}:
            self.eat(self.current_token[0])
            self.termo()

    def termo(self):
        self.fator()
        while self.current_token and self.current_token[0] in {"MULT", "DIV", "MOD"}:
            self.eat(self.current_token[0])
            self.fator()

    def fator(self):
        if self.current_token and self.current_token[0] in {"IDENTIFIER", "NUMBER", "TRUE", "FALSE"}:
            self.eat(self.current_token[0])
        elif self.current_token and self.current_token[0] == "LPAREN":
            self.eat("LPAREN")
            self.expressao()
            self.eat("RPAREN")
        elif self.current_token and self.current_token[0] == "NOT":
            self.eat("NOT")
            self.fator()
        else:
            raise SyntaxError(f"Unexpected token in fator: {self.current_token}")

# Exemplo de uso
if __name__ == "__main__":
    test_files = [
        'tests/atribuicao.txt',
        'tests/chamada_funcao.txt',
        'tests/chamada_procedimento.txt',
        'tests/condicional.txt',
        'tests/declaracao_funcao.txt'
    ]

    for test_file in test_files:
        with open(test_file, 'r') as file:
            code = file.read()
        
        print(f"\nTesting {test_file}...")
        lexer = Lexer(code)
        tokens = lexer.get_tokens()
        print(f"Tokens: {tokens}")
        
        parser = Parser(lexer)
        
        try:
            parser.programa()
            print(f"Parsing of {test_file} completed successfully!")
        except SyntaxError as e:
            print(f"Syntax error in {test_file}: {e}")
        except Exception as e:
            print(f"An error occurred in {test_file}: {e}")
