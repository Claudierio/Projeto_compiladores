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

#### **2. Analisador Sintático (`analisador_sintatico.py`)**

**Função:**  
O analisador sintático utiliza a sequência de tokens fornecida pelo analisador léxico para construir uma estrutura hierárquica que representa a gramática da linguagem. Ele verifica se o código está corretamente estruturado segundo as regras gramaticais e gera relatórios de erros sintáticos. Além disso, o analisador interage com o analisador semântico e o gerador de código de três endereços.

**Componentes Principais:**

- **Classe `Parser`:**
  - **Método `__init__`:** Inicializa o parser com o lexer, define o token atual, inicializa a tabela de símbolos, o analisador semântico e o gerador de código de três endereços.
  - **Método `eat`:** Consome o token atual se ele corresponder ao tipo esperado, ou gera um erro de sintaxe, avançando para o próximo token.
  - **Método `programa`:** Verifica a estrutura geral do programa, começando com a palavra-chave `PROGRAM`, verificando declarações e finalizando com a geração do código de três endereços.
  - **Método `bloco`:** Processa um bloco de código delimitado, entrando e saindo de escopos de variáveis.
  - **Método `comando`:** Identifica o comando atual e direciona para o método específico (declarações, atribuições, chamadas de função, laços, condicionais, etc.).
  - **Método `atribuicao_ou_chamada`:** Lida com atribuições a variáveis e chamadas de procedimentos ou funções.
  - **Método `declaracao_variavel`:** Processa declarações de variáveis, adicionando-as à tabela de símbolos e gerando o código de três endereços.
  - **Método `declaracao_funcao`:** Processa declarações de funções, verifica parâmetros, e gera rótulos para o código de três endereços.
  - **Método `declaracao_procedimento`:** Processa procedimentos de maneira similar às funções, mas sem retorno.
  - **Método `expressao`:** Avalia expressões aritméticas e booleanas, verificando a consistência de tipos e gerando o código correspondente.
  - **Métodos auxiliares:** `fator`, `termo`, `expressao_simples` — lidam com partes de expressões e operadores.

**Novidades:**
- Integração com o **analisador semântico** para verificação de tipos e relatórios de erros semânticos.
- Geração de **código de três endereços** em diversas operações, incluindo atribuições, declarações, condicionais e loops.
- Tratamento de **funções e procedimentos**, com verificação de escopo e compatibilidade de tipos.

**Exemplo de Uso:**  
O arquivo lê um código-fonte, gera tokens via o lexer, e então utiliza o parser para analisar a sintaxe. Erros são reportados, tanto de sintaxe quanto semânticos, e o código de três endereços é gerado e exibido.

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