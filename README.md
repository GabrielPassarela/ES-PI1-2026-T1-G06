# LAD.Py — Sistema de Votação Digital

> Projeto Integrador I – Engenharia de Software | PUC Campinas
> Prof. Dr. Luã Marcelo Muriana — 2026

---

## Descrição do Projeto

O **LAD.Py** é um sistema de votação digital desenvolvido com finalidade exclusivamente didática. O sistema é executado via terminal e integra conhecimentos de **Lógica de Programação em Python**, **Banco de Dados com MySQL** e **Criptografia com Cifra de Hill**.

O sistema permite o cadastro de eleitores e candidatos, a realização de votações com controle de acesso, geração de logs de auditoria e apuração de resultados.

---

## Integrantes

| Nome | RA |
|------|----|
| Gabriel Passarela Silva | 26008264 |
| Felipe Ferles Moratori | 26003809 |
| Miguel Victor de Moraes Horcel | 26000346 |
| Israel Vitor da Cunha | 26011922 |
| Vinicius de Morais Borges de Oliveira | 26011152 |

---

## Aviso

> Este projeto tem finalidade **exclusivamente didática**. É uma simulação acadêmica e **não possui relação** com o funcionamento, as tecnologias ou os sistemas de votação utilizados em processos eleitorais reais.

---

## Tecnologias Utilizadas

| Tecnologia | Descrição |
|------------|-----------|
| Python | Linguagem principal do sistema |
| MySQL | Banco de dados relacional |
| mysql-connector-python | Conexão entre Python e MySQL |
| numpy | Utilizado na implementação da Cifra de Hill |
| datetime | Registro de data e hora nos logs e votos |
| random / string | Geração de chaves de acesso e protocolos |

---

## Estrutura do Projeto

```
ES-PI1-2026-T1-G06/
│
├── src/
│   ├── main.py           # Ponto de entrada, navegação entre menus
│   ├── menus.py          # Funções de exibição dos menus no terminal
│   ├── operacoes.py      # Lógica de negócio de todas as funcionalidades
│   ├── validacao.py      # Validação matemática de CPF e título de eleitor
│   ├── criptografia.py   # Cifra de Hill para criptografar CPF, chave e protocolo
│   ├── database.py       # Conexão com o banco de dados MySQL
│   └── logs.py           # Registro e exibição de logs de ocorrências
│
├── sql/
│   └── projeto_integrador.sql   # Script de criação do banco de dados
│
└── README.md
```

---

## Funcionalidades

### Módulo Gerenciamento
- Cadastro de eleitores com validação de CPF e título de eleitor
- Geração automática de chave de acesso individual
- Edição e remoção de eleitores
- Busca por CPF e listagem de todos os eleitores
- Cadastro, edição, remoção, busca e listagem de candidatos

### Módulo Votação
- Autenticação do mesário com zerézima (limpeza e confirmação de votos zerados)
- Identificação do eleitor por título, CPF e chave de acesso
- Registro de voto com exibição do candidato para confirmação
- Suporte a voto nulo
- Encerramento da votação com dupla confirmação do mesário

### Auditoria
- Exibição de logs de ocorrências com timestamp
- Exibição de protocolos de votação descriptografados

### Resultados
- Boletim de urna com declaração do vencedor
- Estatística de comparecimento
- Votos por partido com percentual
- Validação de integridade entre votos registrados e eleitores que votaram

---

## Segurança e Criptografia

O sistema utiliza a **Cifra de Hill** (baseada em álgebra linear) para proteger os seguintes dados antes de armazená-los no banco:

- **CPF** do eleitor
- **Chave de acesso** do eleitor
- **Protocolo de votação**

---




## Instalação e Execução

**1. Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/ES-PI1-2026-T1-G06.git
cd ES-PI1-2026-T1-G06
```

**2. Instale as dependências:**
```bash
pip install mysql-connector-python numpy
```

**3. Configure o banco de dados:**

- Inicie o MySQL
- Abra um cliente MySQL
- Execute o script `sql/projeto_integrador.sql` para criar o banco e as tabelas

**4. Configure a conexão no arquivo `src/database.py`:**
```python
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='SUA_SENHA_AQUI',
    database='projeto_integrador'
)
```

**5. Execute o sistema:**
```bash
cd src
py main.py
```

---

## Observação sobre o Banco de Dados

O script SQL cria automaticamente as tabelas:

- `ELEITORES` — armazena os dados dos eleitores com CPF e chave de acesso criptografados
- `CANDIDATOS` — armazena os dados dos candidatos
- `VOTOS` — registra os votos com protocolo criptografado, data/hora e candidato escolhido
