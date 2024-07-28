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

#### **3. Programa Principal (`main.py`)**

**Função:**
O programa principal integra o analisador léxico e o analisador sintático. Ele gerencia a execução dos testes e apresenta os resultados.

**Componentes Principais:**
  
- **Função `main`:** 
  - **Leitura dos Arquivos de Teste:** Itera sobre uma lista de arquivos de teste, lê o código fonte e cria instâncias de `Lexer` e `Parser`.
  - **Geração e Impressão de Tokens:** Gera tokens usando o lexer e os imprime.
  - **Parsing e Relatórios:** Usa o parser para verificar a sintaxe dos códigos e imprime o resultado, destacando sucessos e erros com cores.

**Exemplo de Uso:**
O programa lê vários arquivos de teste, processa-os e exibe se o parsing foi bem-sucedido ou se ocorreram erros.