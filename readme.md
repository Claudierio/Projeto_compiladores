### **Projeto Compiladores**

#### **1. Analisador Léxico (`analisador_lexico.py`)**

**Função:**
O analisador léxico é responsável por transformar o código fonte em uma sequência de tokens. Tokens são unidades básicas de significado na linguagem, como palavras-chave, identificadores e operadores.

**Componentes Principais:**

- **Lista de Tokens:** Define os padrões regex para diferentes tipos de tokens, como palavras-chave (`programa`, `if`, `while`), operadores (`+`, `-`, `*`), e outros (`IDENTIFIER`, `NUMBER`, `STRING`).

- **Classe `Lexer`:**
  - **Método `__init__`:** Inicializa o lexer com o código fonte e começa a tokenização.
  - **Método `tokenize`:** Processa o código fonte, reconhecendo tokens baseados nos padrões regex definidos. Ignora espaços em branco e emite um erro para caracteres inválidos.
  - **Método `next_token`:** Retorna o próximo token da lista.
  - **Método `get_tokens`:** Retorna a lista completa de tokens.

**Exemplo de Uso:**
O arquivo inclui um bloco de código que lê arquivos de teste e imprime os tokens gerados.

---

#### **2. Analisador Sintático (`analisador_sintatico.py`)**

**Função:**
O analisador sintático utiliza a sequência de tokens fornecida pelo analisador léxico para construir uma estrutura hierárquica que representa a gramática da linguagem. Ele verifica se o código está corretamente estruturado segundo as regras gramaticais.

**Componentes Principais:**

- **Classe `Parser`:**
  - **Método `__init__`:** Inicializa o parser com o lexer e define o token atual.
  - **Método `eat`:** Consome o token atual se ele corresponder ao tipo esperado, avançando para o próximo token.
  - **Método `programa`:** Verifica a estrutura geral do programa, começando com a palavra-chave `programa` e terminando com um bloco de código.
  - **Método `bloco`:** Processa o bloco de código, que pode conter comandos variados.
  - **Método `comando`:** Decide o tipo de comando com base no token atual e chama o método apropriado (declarações, atribuições, chamadas, etc.).
  - **Método `atribuicao_ou_chamada`:** Trata atribuições e chamadas de funções/procedimentos.
  - **Método `declaracao_variavel`, `declaracao_procedimento`, `declaracao_funcao`, etc.:** Processa declarações específicas e seus componentes.
  - **Método `expressao`:** Avalia expressões aritméticas e booleanas.
  - **Método `fator`, `termo`, `expressao_simples`:** Componentes da análise de expressões, lidando com operações e agrupamentos.

**Exemplo de Uso:**
O arquivo lê arquivos de teste, gera tokens, e então usa o parser para verificar a sintaxe. Erros de sintaxe são capturados e relatados.

---

#### **3. Analisador Semântico (`analisador_semantico.py`)**

**Função:**
O analisador semântico verifica a correção do código em termos de tipos e declarações, garantindo que as variáveis e funções sejam usadas corretamente e que as operações sejam consistentes com seus tipos.

**Componentes Principais:**

- **Classe `SemanticAnalyzer`:**
  - **Método `__init__`:** Inicializa o analisador semântico com a tabela de símbolos e uma lista de erros.
  - **Método `check_variable_declaration`:** Verifica se uma variável foi declarada antes de seu uso.
  - **Método `check_function_declaration`:** Verifica se uma função foi declarada antes de seu uso.
  - **Método `check_function_return`:** Verifica se uma função retorna um valor quando necessário.
  - **Método `check_type_consistency`:** Verifica a consistência de tipos em operações e atribuições.
  - **Método `report_errors`:** Exibe todos os erros semânticos encontrados.

**Exemplo de Uso:**
O arquivo lê e processa a tabela de símbolos e o código, verificando e relatando erros semânticos encontrados.

---

#### **4. Gerador de Código de Três Endereços (`codigo_tres_enderecos.py`)**

**Função:**
O gerador de código de três endereços cria uma representação intermediária do código, facilitando a tradução para código de máquina ou otimizações.

**Componentes Principais:**

- **Classe `ThreeAddressCodeGenerator`:**
  - **Método `__init__`:** Inicializa o gerador com listas de código, contadores de temporários e rótulos.
  - **Método `new_temp`:** Gera um novo nome de variável temporária.
  - **Método `generate`:** Gera uma instrução de três endereços e a adiciona ao código.
  - **Método `print_code`:** Imprime o código de três endereços.
  - **Método `new_label`:** Gera um novo rótulo.

**Exemplo de Uso:**
O arquivo cria e imprime o código de três endereços a partir das instruções geradas.

---

#### **5. Tabela de Símbolos (`tabela_simbolos.py`)**

**Função:**
A tabela de símbolos gerencia a declaração e a busca de variáveis e funções, mantendo informações sobre escopos e símbolos.

**Componentes Principais:**

- **Classe `SymbolTable`:**
  - **Método `__init__`:** Inicializa a tabela de símbolos com escopos global e local.
  - **Método `enter_scope`:** Entra em um novo escopo.
  - **Método `exit_scope`:** Sai do escopo atual.
  - **Método `add_symbol`:** Adiciona um símbolo ao escopo atual ou ao escopo global.
  - **Método `find_symbol`:** Procura um símbolo nos escopos (do mais interno ao mais externo).
  - **Método `print_table`:** Imprime a tabela de símbolos.

**Exemplo de Uso:**
O arquivo gerencia escopos e símbolos, imprimindo a tabela de símbolos atualizada.

---

#### **6. Programa Principal (`main.py`)**

**Função:**
O programa principal integra o analisador léxico, o analisador sintático, o analisador semântico e o gerador de código de três endereços, gerenciando a execução dos testes e apresentando resultados.

**Componentes Principais:**
  
- **Função `main`:**
  - **Leitura dos Arquivos de Teste:** Itera sobre uma lista de arquivos de teste, lê o código fonte e cria instâncias de `Lexer`, `Parser`, `SemanticAnalyzer` e `ThreeAddressCodeGenerator`.
  - **Geração e Impressão de Tokens:** Gera tokens usando o lexer e os imprime.
  - **Parsing e Relatórios:** Usa o parser para verificar a sintaxe dos códigos e imprime o resultado.
  - **Análise Semântica:** Verifica e relata erros semânticos.
  - **Geração de Código:** Gera e imprime o código de três endereços.

**Exemplo de Uso:**
O programa lê vários arquivos de teste, processa-os e exibe se o parsing e a análise semântica foram bem-sucedidos, além de gerar e exibir o código de três endereços.