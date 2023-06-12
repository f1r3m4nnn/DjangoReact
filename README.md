# Teste Django/React

Envolve desenvolvimento e consumo de APIs em uma simulação de controle de pedidos/faturamento.

## Descrição

Subindo a parte em Django. A parte em React estarpa disponível logo mais.

- DRF;
- Acrescentei lógica simplificada para estoque, consumo do estoque, impostos etc;
- Existem automações para popular a base de dados, incluindo uma que tenta simular comportamento humano gerando pedidos. Claro que seria possível adicionar mil critérios e condiçoes, mas colocar mais energia nesse tipo de coisa acabaria fugindo do escopo;
- A idéia era adicionar segurança, também, mas faltou tempo. Estava pensando hoje em Keycloak. Tanto apara autenticação entre os serviços, como para autenticação/autorização de usuários;

Qualquer dúvida contatos abaixo. Valeu!

## Pré-requisitos

- Docker
- Docker Compose

## Configuração do Ambiente de Desenvolvimento

1. Clone o repositório.
2. Navegue até o diretório base.
3. Inicie o ambiente Docker: `docker-compose up`
4. Deve funcionar.

## Contato

Tales - tales@routerlabs.io - Telegram: @talesss