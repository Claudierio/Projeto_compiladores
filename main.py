from analisador_lexico import Lexer
from analisador_sintatico import Parser

# Códigos ANSI para cores
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'

def main():
    test_files = [
        'tests/Todos.txt'
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
            print(f"{Colors.GREEN}Parsing of {test_file} completed successfully!{Colors.RESET}")
        except SyntaxError as e:
            print(f"{Colors.RED}Syntax error in {test_file}: {e}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}An error occurred in {test_file}: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()
