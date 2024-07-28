from analisador_lexico import Lexer
from analisador_sintatico import Parser

def main():
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
        
        print(f"Testing {test_file}...")
        lexer = Lexer(code)
        parser = Parser(lexer)
        
        try:
            parser.programa()
            print("Parsing completed successfully!")
        except SyntaxError as e:
            print(f"Syntax error in {test_file}: {e}")
        except Exception as e:
            print(f"An error occurred in {test_file}: {e}")

if __name__ == "__main__":
    main()
