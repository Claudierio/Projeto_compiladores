class SymbolTable:
    def __init__(self):
        # Lista de todos os escopos criados
        self.all_scopes = []
        self.scopes = []
        self.global_scope = {}
        self.all_scopes.append(('global', self.global_scope))

    def enter_scope(self, scope_name='local'):
        # Entra em um novo escopo, adicionando um novo dicionário
        new_scope = {}
        self.scopes.append(new_scope)
        self.all_scopes.append((scope_name, new_scope))
        print(f"Entering new scope: {scope_name}...")

    def exit_scope(self):
        # Sai do escopo atual, removendo o último dicionário
        if len(self.scopes) > 0:
            print("Exiting scope...")
            self.scopes.pop()
        else:
            raise Exception("Cannot exit global scope.")

    def add_symbol(self, name, symbol_type, var_type, line, column):
        # Adiciona o símbolo ao escopo atual ou ao escopo global
        if len(self.scopes) > 0:
            current_scope = self.scopes[-1]
        else:
            current_scope = self.global_scope

        if name in current_scope:
            print(f"Warning: Redeclaring {symbol_type} '{name}' at line {line}, column {column}")
        current_scope[name] = {
            'type': symbol_type,
            'var_type': var_type,
            'line': line,
            'column': column
        }
        print(f"Symbol '{name}' added to scope: {symbol_type}, type: {var_type}, line: {line}, column: {column}")

    def find_symbol(self, name):
        # Procura o símbolo nos escopos (do mais interno ao mais externo)
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        # Procura no escopo global
        if name in self.global_scope:
            return self.global_scope[name]
        return None

    def print_table(self):
        print("\nSymbol Table:")
        print(f"{'Scope':<15}{'Name':<15}{'Type':<15}{'Var Type':<10}{'Line':<5}{'Column':<5}")
        print("-" * 65)

        for scope_name, scope in self.all_scopes:
            for name, details in scope.items():
                symbol_type = details['type']
                var_type = details['var_type'] if details['var_type'] is not None else "N/A"
                line = details['line'] if details['line'] is not None else "N/A"
                column = details['column'] if details['column'] is not None else "N/A"
                print(f"{scope_name:<15}{name:<15}{symbol_type:<15}{var_type:<10}{line:<5}{column:<5}")
