# API de Processamento de Texto

Esta API foi permite o processamento de texto através de um pipeline pré-treinado que utiliza vetores do Google para uma análise mais ampla dos dados do projeto, obtenção de vetores de palavras utilizando Word2Vec, e predição de valores baseados em modelos treinados, como o RandomForest. A seguir, são descritas as funções e rotas disponíveis na API desenvolvida.

## Índice
1. [Instalação](#instalação)
2. [Configuração](#configuração)
3. [Rotas da API](#rotas-da-api)
    - [/pipeline](#pipeline)
    - [/w2v](#w2v)
    - [/model](#model)
    - [/prescribe](#prescribe)
4. [Descrição das Funções](#descrição-das-funções)
    - [get_word_vector](#get_word_vector)
    - [pipeline](#pipeline-função)
    - [word2vec](#word2vec-função)
    - [model](#model-função)
    - [prescribe](#prescribe-função)

## Instalação

Para instalar e configurar a API, siga os seguintes passos:

1. Clone o repositório:
    ```
    git clone <URL_DO_REPOSITORIO>
    ```
2. Navegue até o diretório do projeto:
    ```
    cd <NOME_DO_DIRETORIO>
    ```
3. Instale as dependências:
    ```
    pip install -r requirements.txt
    ```

## Configuração

Antes de iniciar a API, certifique-se de que os seguintes arquivos estão presentes no diretório `../data`:
- `GoogleNews-vectors-negative300.bin.gz.gz` (modelo Word2Vec)
- `pipeline.joblib` (pipeline pré-treinada)
- `model.pkl` (modelo treinado)
- `BERT_model_and_tokenizer.pkl` (modelo e tokenizer BERT)

## Rotas da API

### `/pipeline`
**Método:** GET

**Descrição:** Processa o texto através de uma pipeline pré-treinada.

**Parâmetros de Query:**
- `text` (opcional): Texto a ser processado. Se não for fornecido, será utilizado o valor padrão vazio.

**Retorno:**
- `text` (str): Tokens processados pelo pipeline.

**Exemplo de Uso:**
```
GET /pipeline?text=i hate uber so much
```

### `/w2v`
**Método:** GET

**Descrição:** Obtém vetores de palavras para uma lista de tokens.

**Parâmetros de Query:**
- `tokens` (opcional): Lista de tokens separados por vírgula. Se não for fornecido, será utilizado o valor padrão vazio.

**Retorno:**
- `list`: Lista contendo a soma de todos os vetores de palavras para os tokens fornecidos.

**Exemplo de Uso:**
```
GET /w2v?tokens=uber,so,much
```

### `/model`
**Método:** GET

**Descrição:** Retorna o valor predito baseado no vetor de palavras.

**Parâmetros de Query:**
- `vectors` (opcional): Lista de vetores de palavras. Se não for fornecido, será utilizado o valor padrão vazio.

**Retorno:**
- `json`: Objeto JSON com a chave `predictions` contendo 1, 0 ou -1.

**Exemplo de Uso:**
```
GET /model?vectors=[0.43798828125,0.1256103515625,...]
```

### `/prescribe`
**Método:** GET

**Descrição:** Retorna o valor predito baseado em um texto.

**Parâmetros de Query:**
- `text` (opcional): Texto a ser processado. Se não for fornecido, será utilizado o valor padrão vazio.

**Retorno:**
- `json`: Objeto JSON com a chave predictions contendo 1 (Negativo) ou 0 (Não Negativo).

**Exemplo de Uso:**
```
GET /prescribe?text=i hate uber so much
```

## Descrição das Funções

### `get_word_vector`
**Descrição:** Transforma uma palavra em uma lista de componentes do vetor dessa palavra.

**Argumentos:**
- `word` (str): Uma única palavra.

**Retorno:**
- Se o vetor da palavra não estiver disponível, retorna `None`. Caso contrário, retorna a lista de componentes que formam o vetor.

### `pipeline` (função)
**Descrição:** Processa o texto através de uma pipeline pré-treinada.

**Argumentos:**
- `text` (str): Texto a ser processado. Padrão é uma string vazia.

**Retorno:**
- `text` (str): Tokens processados pelo pipeline.

### `word2vec` (função)
**Descrição:** Obtém vetores de palavras para uma lista de tokens.

**Argumentos:**
- `tokens` (str): Lista de tokens separados por vírgula. Padrão é uma string vazia.

**Retorno:**
- `list`: Lista contendo a soma de todos os vetores de palavras para os tokens fornecidos.

### `model` (função)
**Descrição:** Retorna o valor predito baseado no vetor de palavras.

**Argumentos:**
- `vectors` (str): Lista de vetores de palavras. Padrão é uma string vazia.

**Retorno:**
- `json`: Objeto JSON com a chave `predictions` contendo 1, 0 ou -1.

### `prescribe` (função)
**Descrição:** Retorna o valor predito baseado em um texto.

**Argumentos:**
- `text` (str): Texto a ser processado. Padrão é uma string vazia.

**Retorno:**
- `json`: Objeto JSON com a chave predictions contendo 1 (Negativo) ou 0 (Não Negativo).
