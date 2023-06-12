    CENTRO PAULA SOUZA
    Faculdade de Tecnologia de Ribeirão Preto
    Análise e Desenvolvimento de Sistemas


## **Tópicos Especiais em Informática**
### LUCAS DOS SANTOS DOURADO
## *Projeto Prático*
<br>

# Objetivo
    Desenvolver uma aplicação utilizando a linguagem de programação Python de acordo com o tema escolhido em Sala de Aula

# Requisitos

- **[3.0 pontos] Implementação de pelo menos dez UI (Obrigatorio: Login, sobre, Menu).**
#### *Resultados*:
    01. Login
    02. Sobre
    03. Menu
    04. Lista
    05. Favoritas
    06. Exportar
    07. Confirmar Exportar
    08. Bybit info
    09. Logout
    10. Confirmar Logout
<br>

- **[3.0 pontos] Modelagem do número mínimo de tabelas e implementação das operações (Minimo 3 Tabelas, com CRUD).**
#### *Resultados*:
    Implementado 4 tabelas:
        MAKETATUAL |Tabela temporária para atualização dos dados
        -----------------------------------------------------------------------------
        MARKETANTG |Tabela que armazena os dados baixados efetivos
        -----------------------------------------------------------------------------
        LOGERROS   |Tabela que armazena os erros das moedas que não foram baixadas
        -----------------------------------------------------------------------------
        FAVORITAS  |Tabela para armazenar os pair de moedas favoritados

    Implementadas operações:
        - CREATE
        - INSERT
        - DELETE
        - UPDATE
        - SELECT

    SGBD escolhido:
        SQLITE3
<br>

- **[2.0 pontos] Codificação da funcionalidade para exportação de dados no formato JSON (zip).**
#### *Resultados*:
    Funcionalidade criada com sucesso em uma UI específica.
<br>

- **[2.0 pontos] Implementação da funcionalidade para importação dos dados.**
#### *Resultados*:
    Dados importados através da API da plataforma BYBIT, realizando o insert no sqlite.
