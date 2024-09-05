class SymbolTable:
    def __init__(self):
        # Usamos uma lista de dicionários para simular a pilha de escopos
        self.scopes = [{}]

    def enter_scope(self):
        # Entra em um novo escopo, adicionando um novo dicionário
        self.scopes.append({})

    def exit_scope(self):
        # Sai do escopo atual, removendo o último dicionário
        if len(self.scopes) > 1:
            self.scopes.pop()
        else:
            raise Exception("Cannot exit global scope.")

    def add_symbol(self, name, symbol_type, var_type, line, column):
        current_scope = self.scopes[-1]
        if name in current_scope:
            existing_symbol = current_scope[name]
            if symbol_type == 'function' and existing_symbol['type'] == 'function':
                print(f"Redefining function '{name}' at line {line}, column {column}")
            elif symbol_type == 'variable' and existing_symbol['type'] == 'variable':
                print(f"Redeclaring variable '{name}' at line {line}, column {column}")
            else:
                print(f"Redeclaring {symbol_type} '{name}' at line {line}, column {column}")
        current_scope[name] = {'type': symbol_type, 'var_type': var_type, 'line': line, 'column': column}


    def find_symbol(self, name):
        # Procura o símbolo em todos os escopos (do mais interno ao mais externo)
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def print_table(self):
        print("\nSymbol Table:")
        print(f"{'Scope':<10}{'Name':<15}{'Type':<10}{'Var Type':<10}{'Line':<5}{'Column':<5}")
        print("-" * 55)
        for i, scope in enumerate(self.scopes):
            for name, details in scope.items():
                # Formatar os tipos e garantir que não temos None
                symbol_type = details['type']
                var_type = details['var_type'] if details['var_type'] is not None else "N/A"
                line = details['line'] if details['line'] is not None else "N/A"
                column = details['column'] if details['column'] is not None else "N/A"
                
                print(f"{i:<10}{name:<15}{symbol_type:<10}{var_type:<10}{line:<5}{column:<5}")

# Exemplo de uso
symbol_table = SymbolTable()

