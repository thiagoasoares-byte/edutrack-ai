# Subjects API CRUD Specification

## Purpose

Define os requisitos para criar um conjunto completo de endpoints REST (Create, Read, Update, Delete) que permitam gerenciar disciplinas acadêmicas. Os endpoints devem garantir que cada usuário acesse apenas suas próprias disciplinas, protegendo a integridade dos dados.

## ADDED Requirements

### Requirement: Criar endpoint POST /subjects

Sistema SHALL permitir que usuários autenticados criem novas disciplinas fornecendo nome e descrição opcionais.

#### Scenario: Usuário cria uma nova disciplina com sucesso
- **WHEN** usuário autenticado envia POST com `name` válido
- **THEN** sistema cria a disciplina associada ao `user_id` do usuário e retorna 201 Created com objeto completo

#### Scenario: Usuário tenta criar disciplina sem name
- **WHEN** usuário envia POST sem o campo `name`
- **THEN** sistema retorna 400 Bad Request com mensagem de erro

---

### Requirement: Criar endpoint GET /subjects

Sistema SHALL retornar lista de todas as disciplinas pertencentes ao usuário autenticado.

#### Scenario: Usuário lista suas disciplinas
- **WHEN** usuário autenticado acessa GET /subjects
- **THEN** sistema retorna 200 OK com array contendo todas as disciplinas do usuário

#### Scenario: Usuário não autenticado tenta listar
- **WHEN** requisição é feita sem token de autenticação
- **THEN** sistema retorna 401 Unauthorized

---

### Requirement: Criar endpoint GET /subjects/{id}

Sistema SHALL retornar detalhes de uma disciplina específica após validar que pertence ao usuário autenticado.

#### Scenario: Usuário consulta sua disciplina
- **WHEN** usuário autenticado acessa GET /subjects/{id} de sua propriedade
- **THEN** sistema retorna 200 OK com detalhes da disciplina

#### Scenario: Usuário tenta acessar disciplina de outro usuário
- **WHEN** usuário tenta acessar GET /subjects/{id} de outro usuário
- **THEN** sistema retorna 403 Forbidden ou 404 Not Found

#### Scenario: Disciplina não existe
- **WHEN** usuário acessa GET /subjects/{id} com ID inexistente
- **THEN** sistema retorna 404 Not Found

---

### Requirement: Criar endpoint PATCH /subjects/{id}

Sistema SHALL permitir que usuários atualizem seus dados de disciplina após validar propriedade.

#### Scenario: Usuário atualiza sua disciplina
- **WHEN** usuário autenticado envia PATCH /subjects/{id} com campos válidos
- **THEN** sistema atualiza apenas os campos fornecidos e retorna 200 OK com objeto atualizado

#### Scenario: Usuário tenta atualizar disciplina de outro usuário
- **WHEN** usuário tenta fazer PATCH /subjects/{id} de outro usuário
- **THEN** sistema retorna 403 Forbidden ou 404 Not Found

#### Scenario: Atualização com dados inválidos
- **WHEN** usuário envia PATCH com `name` vazio ou nulo
- **THEN** sistema retorna 400 Bad Request

---

### Requirement: Criar endpoint DELETE /subjects/{id}

Sistema SHALL permitir que usuários deletem suas próprias disciplinas após validar propriedade.

#### Scenario: Usuário deleta sua disciplina
- **WHEN** usuário autenticado envia DELETE /subjects/{id} de sua propriedade
- **THEN** sistema deleta o registro e retorna 204 No Content

#### Scenario: Usuário tenta deletar disciplina de outro usuário
- **WHEN** usuário tenta fazer DELETE /subjects/{id} de outro usuário
- **THEN** sistema retorna 403 Forbidden ou 404 Not Found

#### Scenario: Tentativa de deletar disciplina inexistente
- **WHEN** usuário envia DELETE /subjects/{id} com ID inexistente
- **THEN** sistema retorna 404 Not Found

---

### Requirement: Validar autenticação em todos os endpoints

Sistema SHALL rejeitar requisições sem autenticação válida em todos os endpoints CRUD.

#### Scenario: Requisição sem token
- **WHEN** cliente faz requisição sem token de autenticação
- **THEN** sistema retorna 401 Unauthorized

#### Scenario: Requisição com token inválido
- **WHEN** cliente envia token expirado ou malformado
- **THEN** sistema retorna 401 Unauthorized

---

### Requirement: Filtrar resultados por user_id

Sistema SHALL garantir que cada usuário vê apenas seus próprios dados em todas as operações.

#### Scenario: GET /subjects retorna apenas disciplinas do usuário
- **WHEN** usuário A faz GET /subjects
- **THEN** sistema retorna SOMENTE disciplinas onde `user_id` corresponde ao usuário A

#### Scenario: GET /subjects/{id} valida propriedade
- **WHEN** usuário A tenta acessar GET /subjects/{id} onde disciplina pertence a usuário B
- **THEN** sistema retorna 403 Forbidden ou 404 Not Found (nunca revelando a existência)

---

### Requirement: Retornar status HTTP apropriados

Sistema SHALL usar códigos de status HTTP padrão para indicar resultado de operações.

#### Scenario: Create bem-sucedido
- **WHEN** POST /subjects cria disciplina com sucesso
- **THEN** sistema retorna 201 Created

#### Scenario: Update bem-sucedido
- **WHEN** PATCH /subjects/{id} atualiza disciplina com sucesso
- **THEN** sistema retorna 200 OK

#### Scenario: Delete bem-sucedido
- **WHEN** DELETE /subjects/{id} deleta disciplina com sucesso
- **THEN** sistema retorna 204 No Content

#### Scenario: Erro de validação
- **WHEN** entrada contém dados inválidos
- **THEN** sistema retorna 400 Bad Request

#### Scenario: Recurso não encontrado
- **WHEN** ID fornecido não existe
- **THEN** sistema retorna 404 Not Found
