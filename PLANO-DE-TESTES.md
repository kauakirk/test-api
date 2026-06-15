# PLANO-DE-TESTES

## Objetivo da suíte

O objetivo desta suíte de testes é validar o comportamento da API de usuários e garantir que os principais fluxos de cadastro, autenticação e gerenciamento de usuário funcionem corretamente. O foco inicial é oferecer confiança na camada de API REST do serviço público `https://compassuol.serverest.dev` e suportar a evolução dos testes conforme o desafio avança.

## Estratégia

- Tipo de teste: Testes de API automatizados.
- Camada: camada de integração / contrato da API, com foco na validação de endpoints REST.
- Ferramentas: Python, Requests e Pytest.
- Abordagem: validar respostas HTTP, contratos JSON, fluxos de criação/edição/exclusão de usuários e tratamento de erros.

## Escopo

### Coberto

- Endpoints de usuários:
  - `GET /usuarios` - listar usuários
  - `POST /usuarios` - criar usuário
  - `GET /usuarios` com filtro por `_id` - buscar usuário por ID
  - `PUT /usuarios/{_id}` - editar usuário
  - `DELETE /usuarios/{_id}` - excluir usuário
- Endpoint de autenticação:
  - `POST /login` - login de usuário
- Regras de negócio importantes:
  - não permitir cadastro com email já existente
  - não permitir edição para email já utilizado por outro usuário
  - permitir criação de usuário via PUT em ID inexistente, conforme comportamento observado
  - validar mensagens e códigos de status esperados

### Fora do escopo inicial

- Endpoints de produtos (`/produtos`)
- Endpoints de carrinhos (`/carrinhos`)
- Testes de performance ou carga
- Testes de segurança (autenticação/autorizações complexas) além do login básico
- Testes de UI ou frontend

## Cenários a implementar

### Endpoint `GET /usuarios`

- Deve retornar status `200` e lista de usuários
- Deve retornar os campos esperados `quantidade` e `usuarios`

### Endpoint `POST /usuarios`

- Deve criar um usuário com sucesso e retornar `201`
- Deve falhar com `400` quando `email` estiver ausente
- Deve falhar com `400` quando o email já estiver em uso

### Endpoint `POST /login`

- Deve autenticar um usuário válido e retornar `200`
- Deve retornar token/autorização no corpo da resposta
- Deve falhar com credenciais inválidas (próximo passo)

### Endpoint `GET /usuarios?_id={id}`

- Deve retornar o usuário correto ao buscar por ID
- Deve retornar `quantidade` igual a `1` e o usuário esperado

### Endpoint `PUT /usuarios/{id}`

- Deve editar um usuário existente e retornar `200`
- Deve permitir criar um novo usuário via `PUT` em ID inexistente e retornar `201`
- Deve falhar com `400` ao tentar editar um usuário para um email já existente

### Endpoint `DELETE /usuarios/{id}`

- Deve excluir usuário existente e retornar mensagem de sucesso
- Deve retornar comportamento consistente quando o usuário não existe

## Critérios de qualidade

- Um teste está pronto quando:
  - valida o status HTTP esperado
  - valida o corpo da resposta e os campos essenciais
  - isola o caso de teste criando dados únicos quando necessário
  - não depende de dados de outros testes
  - roda de forma confiável em sequência e em execução isolada
  - documenta claramente o objetivo do caso de teste

## Observações iniciais

- A API pública do ServeRest tem documentação disponível em `https://compassuol.serverest.dev/` e `https://compassuol.serverest.dev/swagger.json?lang=pt-BR`.
- Este documento deve ser atualizado sempre que novos endpoints, regras de negócio ou critérios forem adicionados.
