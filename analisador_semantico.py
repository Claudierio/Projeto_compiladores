from tabela_simbolos import SymbolTable

class SemanticAnalyzer:
    def __init__(self, symbolTable):
        self.symbolTable = symbolTable
        self.errors = []

    def check_variable_declaration(self, identifier, line, column):
        """Verifica se a variável foi declarada antes de seu uso."""
        symbol = self.symbolTable.find_symbol(identifier)
        if not symbol:
            self.errors.append(f"Semantic error: Undeclared variable '{identifier}' at line {line}, column {column}")

    def check_function_declaration(self, func_name, line, column):
        """Verifica se a função foi declarada antes de seu uso."""
        symbol = self.symbolTable.find_symbol(func_name)
        if not symbol or symbol['type'] != 'function':
            self.errors.append(f"Semantic error: Undeclared function '{func_name}' at line {line}, column {column}")

    def check_type_consistency(self, left_type, right_type, line, column):
        """Verifica a consistência de tipos em operações e atribuições."""
        if left_type != right_type:
            self.errors.append(f"Semantic error: Type mismatch at line {line}, column {column}: "
                               f"{left_type} cannot be assigned to {right_type}")

    def report_errors(self):
        """Exibe todos os erros semânticos encontrados."""
        if not self.errors:
            print("\nNo semantic errors found.")
        else:
            print("\nSemantic Errors:")
            for error in self.errors:
                print(error)
