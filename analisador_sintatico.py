from analisador_lexico import Lexer
from tabela_simbolos import SymbolTable
from analisador_semantico import SemanticAnalyzer
from codigo_tres_enderecos import ThreeAddressCodeGenerator

class Parser: 
    #Inicializa o parser com o lexer e define o token atual.
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next_token()
        self.symbol_table = SymbolTable()  # Adicione a tabela de símbolos aqui
        self.semantic_analyzer = SemanticAnalyzer(self.symbol_table)  # Adicione o analisador semântico aqui
        self.code_generator = ThreeAddressCodeGenerator()  # Adicione o gerador de código de três endereços aqui


    #Consome o token atual se ele corresponder ao tipo esperado, avançando para o próximo token.
    def eat(self, token_type):
        if self.current_token and self.current_token[0] == token_type:
            self.current_token = self.lexer.next_token()
        else:
            line = self.current_token[2] if self.current_token else "EOF"
            column = self.current_token[3] if self.current_token else "EOF"
            raise SyntaxError(f"Expected {token_type}, got {self.current_token} at line {line}, column {column}")
    #Verifica a estrutura geral do programa, começando com a palavra-chave programa e terminando com um bloco de código.
    def programa(self):
        self.eat("PROGRAM")
        self.eat("IDENTIFIER")
        self.eat("SEMICOLON")
        self.bloco()
        if self.current_token:
            raise SyntaxError(f"Unexpected token at the end of program: {self.current_token}")
        self.symbol_table.print_table()  # Print the symbol table at the end
        # Relata erros semânticos, se houver
        self.semantic_analyzer.report_errors()
        # Imprime o código de três endereços gerado
        self.code_generator.print_code()
    #Processa o bloco de código, que pode conter comandos variados.
    def bloco(self):
        self.symbol_table.enter_scope()  # Entra no escopo do bloco
        while self.current_token and self.current_token[0] in {
            "PROCEDURE", "FUNCTION", "INT", "BOOL", "IDENTIFIER",
            "IF", "WHILE", "RETURN", "CONTINUE", "BREAK", "PRINT"
        }:
            self.comando()
        self.symbol_table.exit_scope()  # Sai do escopo do bloco
    #Decide o tipo de comando com base no token atual e chama o método apropriado (declarações, atribuições, chamadas, etc.).
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
        
    #Trata atribuições e chamadas de funções/procedimentos.
    def atribuicao_ou_chamada(self):
        identifier = self.current_token[1]  # Pegando o nome do identificador (ex: "c")
        print(f"Processing assignment or function call for: {identifier}")
        line = self.current_token[2]       # Linha do identificador
        column = self.current_token[3]     # Coluna do identificador
        self.eat("IDENTIFIER")
        
        if self.current_token[0] == "ASSIGN":
            self.eat("ASSIGN")
            print(f"Assignment detected for variable: {identifier}")
            
            # Recuperar o símbolo da variável da tabela de símbolos
            symbol = self.symbol_table.find_symbol(identifier)
            if not symbol:
                self.semantic_analyzer.errors.append(
                    f"Semantic error: Undeclared variable '{identifier}' at line {line}, column {column}"
                )
                return
            
            left_type = symbol['var_type']  # Tipo da variável (ex: "INT" para "c")
            print(f"Left side type (variable '{identifier}'): {left_type}")
            
            # Obter o tipo da expressão à direita (ex: "10" -> tipo "INT")
            right_type = self.expressao()  # Aqui esperamos receber "INT"
            print(f"Right side type (expression): {right_type}")
            
            # Verificar a consistência de tipos
            if left_type != right_type:
                self.semantic_analyzer.errors.append(f"Semantic error: Type mismatch at line {line}, column {column}: variable '{identifier}' cannot be assigned to {right_type}")
            else:
                print(f"Correct attribution: '{identifier}' of type {left_type} receive {right_type}")
                self.code_generator.generate('ASSIGN', right_type, None, identifier)
                print(f"Generated three-address code for assigning {right_type} to {identifier}")

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
        
    #Processa declarações específicas e seus componentes.
    def declaracao_variavel(self):
        var_type = self.current_token[0]  # INT ou BOOL
        self.eat(var_type)
        
        var_name = self.current_token[1]  # IDENTIFIER
        line = self.current_token[2]      # Linha do token
        column = self.current_token[3]    # Coluna do token
        
        self.eat("IDENTIFIER")
        self.eat("SEMICOLON")
        
        # Adicionar o símbolo à tabela de símbolos com a linha e coluna corretas
        self.symbol_table.add_symbol(var_name, 'variable', var_type, line, column)

        # Print para debug: verificar se a variável foi adicionada corretamente
        print(f"Variable declared: {var_name}, type: {var_type}, at line {line}, column {column}")

    def declaracao_funcao(self):
        self.eat("FUNCTION")
        return_type = self.current_token[0]  # INT ou BOOL
        self.eat("INT")
        
        func_name = self.current_token[1]  # IDENTIFIER
        line = self.current_token[2]
        column = self.current_token[3]
        
        self.eat("IDENTIFIER")
        
        if self.symbol_table.find_symbol(func_name):
            print(f"Function '{func_name}' already declared. Redefining it.")
        
        # Adicionar a função na tabela de símbolos
        self.symbol_table.add_symbol(func_name, 'function', return_type, line, column)
        
        self.eat("LPAREN")
        
        # Processar parâmetros da função, se existirem
        if self.current_token and self.current_token[0] in {"INT", "BOOL"}:
            self.parametro()  # Consome o primeiro parâmetro
            while self.current_token and self.current_token[0] == "COMMA":  # Se houver mais de um parâmetro
                self.eat("COMMA")
                self.parametro()  # Consome o próximo parâmetro
        
        # Consome o parêntese direito ")"
        self.eat("RPAREN")
        
        # Consome a chave de abertura "{"
        self.eat("LBRACE")
        
        # Analisa o bloco de comandos dentro da função
        self.bloco()
        
        # Consome a chave de fechamento "}"
        self.eat("RBRACE")

    def declaracao_procedimento(self):
        self.eat("PROCEDURE")
        proc_name = self.current_token[1]  # IDENTIFIER
        line = self.current_token[2]
        column = self.current_token[3]
        
        self.eat("IDENTIFIER")
        
        if self.symbol_table.find_symbol(proc_name):
            print(f"Procedure '{proc_name}' already declared. Redefining it.")
        
        # Adicionar o procedimento na tabela de símbolos
        self.symbol_table.add_symbol(proc_name, 'procedure', None, line, column)
        
        self.eat("LPAREN")
        
        # Processar parâmetros do procedimento, se existirem
        if self.current_token and self.current_token[0] in {"INT", "BOOL"}:
            self.parametro()  # Consome o primeiro parâmetro
            while self.current_token and self.current_token[0] == "COMMA":  # Se houver mais de um parâmetro
                self.eat("COMMA")
                self.parametro()  # Consome o próximo parâmetro
        
        # Consome o parêntese direito ")"
        self.eat("RPAREN")
        self.eat("LBRACE")
        self.bloco()
        self.eat("RBRACE")



    def declaracao_if(self):
        self.eat("IF")
        self.eat("LPAREN")
        self.expressao() 
        self.eat("RPAREN")
        self.eat("LBRACE")
        self.bloco()  
        self.eat("RBRACE")
        self.eat("FIM_IF") 
        
        # Processa a parte else opcional
        self.declaracao_else()

    def declaracao_else(self):
        if self.current_token and self.current_token[0] == "ELSE":
            self.eat("ELSE")
            self.eat("LBRACE")
            self.bloco()  
            self.eat("RBRACE")
            self.eat("FIM_ELSE")  # Consome o "fim_else"
        elif self.current_token and self.current_token[0] == "FIM_ELSE" and self.current_token[1] == "fim_else":
            self.eat("FIM_ELSE")  


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
        
        if self.current_token[0] != "FIM_WHILE" or self.current_token[1] != "fim_while":
            raise SyntaxError(f"Expected 'fim_while', got {self.current_token}")
        
        self.eat("FIM_WHILE")  # Consome o "fim_while"

    def declaracao_retorno(self):
        self.eat("RETURN")
        expr_type = self.expressao()
        
        # Verifique se o tipo de retorno é compatível com o tipo da função
        if expr_type != "INT":  # Supondo que a função soma seja do tipo INT
            line, column = self.current_token[2], self.current_token[3]
            self.semantic_analyzer.errors.append(
                f"Semantic error: Type mismatch in return at line {line}, column {column}. Expected INT, got {expr_type}"
            )
    
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
        #self.eat(self.current_token[0])  # INT ou BOOL
        var_type = self.current_token[0]
        self.eat(var_type)
        var_name = self.current_token[1]
        line = self.current_token[2]
        column = self.current_token[3]
        self.eat("IDENTIFIER")
        self.symbol_table.add_symbol(var_name, 'parameter', var_type, line, column)
        print(f"Parameter added: {var_name}, type: {var_type}, line: {line}, column: {column}")

    #Avalia expressões aritméticas e booleanas.
    def expressao(self):
        expr_type = self.expressao_simples()
        if self.current_token and self.current_token[0] in {"EQ", "NEQ", "GT", "LT", "GTE", "LTE"}:
            operator = self.current_token[0]
            self.eat(operator)
            right_expr_type = self.expressao_simples()
            
            # Verificar se os tipos de ambos os lados da expressão são compatíveis
            if expr_type != right_expr_type:
                line, column = self.current_token[2], self.current_token[3]
                self.semantic_analyzer.errors.append(f"Semantic error: Type mismatch in comparison at line {line}, column {column}")
            
            # return "BOOL"  # O resultado de comparações é sempre booleano
        return expr_type

    #Componentes da análise de expressões, lidando com operações e agrupamentos.
    def expressao_simples(self):
        if self.current_token and self.current_token[0] in {"PLUS", "MINUS"}:
            self.eat(self.current_token[0])
        
        expr_type = self.termo()
        
        while self.current_token and self.current_token[0] in {"PLUS", "MINUS"}:
            operator = self.current_token[0]
            self.eat(operator)
            
            right_expr_type = self.termo()
            
            if expr_type != "INT" or right_expr_type != "INT":
                line, column = self.current_token[2], self.current_token[3]
                self.semantic_analyzer.errors.append(
                    f"Semantic error: Type mismatch in arithmetic operation at line {line}, column {column}"
                )
            else:
                print(f"Valid arithmetic operation: {expr_type} {operator} {right_expr_type}")
        
        return expr_type


    def termo(self):
        left_type = self.fator()
        while self.current_token and self.current_token[0] in {"MULT", "DIV", "MOD"}:
            operator = self.current_token[0]
            self.eat(operator)
            right_type = self.fator()

            if left_type != "INT" or right_type != "INT":
                line, column = self.current_token[2], self.current_token[3]
                self.semantic_analyzer.errors.append(
                    f"Semantic error: Type mismatch in operation at line {line}, column {column}. Expected INT, got {left_type} {operator} {right_type}"
                )
        return left_type


    def fator(self):
        if self.current_token[0] == "NUMBER":
            self.eat("NUMBER")
            return "INT"
        elif self.current_token[0] in {"TRUE", "FALSE"}:
            self.eat(self.current_token[0])
            return "BOOL"
        elif self.current_token[0] == "IDENTIFIER":
            identifier = self.current_token[1]
            symbol = self.symbol_table.find_symbol(identifier)
            
            if symbol:
                self.eat("IDENTIFIER")
                return symbol['var_type']  # Retorna o tipo do identificador (INT ou BOOL)
            else:
                line, column = self.current_token[2], self.current_token[3]
                self.semantic_analyzer.errors.append(
                    f"Semantic error: Undeclared variable '{identifier}' at line {line}, column {column}"
                )
                return None
        elif self.current_token[0] == "LPAREN":
            self.eat("LPAREN")
            expr_type = self.expressao()
            self.eat("RPAREN")
            return expr_type
        elif self.current_token[0] == "NOT":
            self.eat("NOT")
            return self.fator()
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
        #print(f"Tokens: {tokens}")
        
        parser = Parser(lexer)
        
        try:
            parser.programa()
            print(f"Parsing of {test_file} completed successfully!")

            # Adicione o trecho aqui:
            if not parser.semantic_analyzer.errors:
                print("\nThree-Address Code:")
                parser.code_generator.print_code()
            else:
                print("Errors were found during semantic analysis. Three-Address Code not generated.")

        except SyntaxError as e:
            print(f"Syntax error in {test_file}: {e}")
        except Exception as e:
            print(f"An error occurred in {test_file}: {e}")
