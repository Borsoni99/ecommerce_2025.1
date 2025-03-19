# Projeto E-commerce com Big Data e Cloud

Este repositório contém um projeto de e-commerce completo, com foco em análise de vendas utilizando Big Data e serviços de Cloud. A solução inclui um **API Gateway**, um **Backend** hospedado em **Azure App Service**, bancos de dados NoSQL (Azure Cosmos DB) e Relacional (Azure SQL), além de um pipeline de Big Data simplificado com integração ao **Power BI** para criação de relatórios.

## Sumário
- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Fluxo de Trabalho](#fluxo-de-trabalho)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Funcionalidades Principais](#funcionalidades-principais)
- [Como Executar](#como-executar)
- [Testes](#testes)
- [Contribuição](#contribuição)
- [Licença](#licença)

---

## Visão Geral
Este projeto simula um e-commerce que permite:
- **Compras de produtos** por usuários autenticados.
- **Verificação de saldo** em cartão de crédito antes de confirmar a compra.
- **Administração de produtos** (CRUD).
- **Relatórios de vendas** usando um pipeline de Big Data.

A aplicação está organizada de forma a mostrar boas práticas de desenvolvimento em Cloud, com alto grau de escalabilidade e observabilidade, além de destacar integrações automatizadas via GitHub Actions e testes de unidade no Backend.

---

## Arquitetura
A arquitetura principal do projeto é composta por:
1. **API Gateway (Azure API Management)**  
   - Responsável por gerenciar e rotear requisições.
   - Endpoints principais:
     - `POST /pedido` → Criar um pedido  
     - `GET /produtos` → Listar produtos  
     - `POST /produto` → Criar um novo produto  
     - `PUT /produto/{id}` → Atualizar um produto  
     - `DELETE /produto/{id}` → Remover um produto  
     - `POST /usuario` → Criar um usuário com cartão de crédito  
     - `PUT /usuario/{id}` → Atualizar informações do usuário  
     - `GET /relatorio-vendas` → Gerar relatório de vendas  

2. **Backend (Azure App Service)**  
   - Lida com a lógica de negócios.
   - Criação de pedidos, gestão de produtos, verificação de saldo e envio de dados para análise.

3. **Bancos de Dados**  
   - **NoSQL (Azure Cosmos DB)**: Armazena informações de produtos e pedidos.  
   - **Relacional (Azure SQL Database)**: Armazena dados de usuários (incluindo saldo de cartão).

4. **Pipeline de Big Data**  
   - Ingestão de dados via **Azure Event Hubs**.  
   - Processamento e transformação com **Azure Data Factory**.  
   - Visualização e criação de relatórios com **Power BI**.

---

## Fluxo de Trabalho
1. O usuário acessa o e-commerce e se cadastra, fornecendo informações de cartão de crédito e saldo inicial.
2. O usuário seleciona produtos e cria um pedido.
3. O sistema **verifica o saldo** do cartão de crédito.
4. Se houver saldo suficiente, o pedido é confirmado e o saldo é atualizado. Caso contrário, a compra é recusada.
5. Os dados do pedido são armazenados no banco de dados via Backend.
6. Paralelamente, as **informações de vendas** são enviadas para o pipeline de Big Data.
7. O pipeline processa os dados e gera relatórios para visualização no Power BI.

---

## Tecnologias Utilizadas
- **Linguagem de Programação**: (ex.: Python, Node.js, .NET – dependendo da sua implementação)
- **API Gateway**: Azure API Management
- **Backend**: Azure App Service
- **Banco de Dados**:
  - Azure Cosmos DB (NoSQL)
  - Azure SQL Database (Relacional)
- **Big Data**:
  - Azure Event Hubs (ingestão de dados)
  - Azure Data Factory (processamento)
- **Visualização**: Power BI
- **Deploy Automatizado**: GitHub Actions
- **Testes Automatizados**: Testes de unidade no backend

---

## Funcionalidades Principais
- **Gestão de Usuários**:
  - Criação e atualização de usuários com informações de cartão de crédito.
  - Verificação e atualização de saldo.
  
- **Gestão de Produtos**:
  - Criação, leitura, atualização e exclusão de produtos (CRUD).

- **Processamento de Pedidos**:
  - Validação de saldo antes da compra.
  - Débito automático do valor do pedido no cartão do usuário, se aprovado.

- **Relatórios de Vendas**:
  - Envio de dados de vendas para o pipeline de Big Data.
  - Relatórios e dashboards para análise de métricas e desempenho de vendas via Power BI.

---


