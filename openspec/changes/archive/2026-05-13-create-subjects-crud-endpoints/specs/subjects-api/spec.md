## ADDED Requirements

### Requirement: Criar um Subject
O sistema DEVE permitir que um usuário autenticado crie um novo `subject`.

#### Scenario: Criação bem-sucedida de um subject
- **WHEN** um usuário autenticado envia uma requisição POST para `/subjects` com dados válidos.
- **THEN** o sistema DEVE criar um novo registro de `subject` na tabela `subjects`.
- **AND** o campo `user_id` do novo registro DEVE ser preenchido com o ID do usuário autenticado.
- **AND** o sistema DEVE retornar o `subject` recém-criado com um status HTTP 201.

#### Scenario: Tentativa de criação não autenticada
- **WHEN** um usuário não autenticado envia uma requisição POST para `/subjects`.
- **THEN** o sistema DEVE retornar um erro de "Não Autenticado" com um status HTTP 401.

### Requirement: Listar Subjects
O sistema DEVE permitir que um usuário autenticado liste apenas seus próprios `subjects`.

#### Scenario: Listagem bem-sucedida de subjects
- **WHEN** um usuário autenticado envia uma requisição GET para `/subjects`.
- **THEN** o sistema DEVE retornar uma lista de `subjects` onde o `user_id` corresponde ao ID do usuário autenticado.
- **AND** o sistema DEVE retornar um status HTTP 200.

#### Scenario: Tentativa de listagem não autenticada
- **WHEN** um usuário não autenticado envia uma requisição GET para `/subjects`.
- **THEN** o sistema DEVE retornar um erro de "Não Autenticado" com um status HTTP 401.

### Requirement: Obter um Subject específico
O sistema DEVE permitir que um usuário autenticado obtenha um `subject` específico que ele possui.

#### Scenario: Obtenção bem-sucedida de um subject
- **WHEN** um usuário autenticado envia uma requisição GET para `/subjects/{id}` para um `subject` que ele possui.
- **THEN** o sistema DEVE retornar os detalhes do `subject` solicitado.
- **AND** o sistema DEVE retornar um status HTTP 200.

#### Scenario: Tentativa de obter um subject de outro usuário
- **WHEN** um usuário autenticado envia uma requisição GET para `/subjects/{id}` para um `subject` que ele não possui.
- **THEN** o sistema DEVE retornar um erro de "Não Autorizado" com um status HTTP 403.

#### Scenario: Tentativa de obter um subject inexistente
- **WHEN** um usuário autenticado envia uma requisição GET para `/subjects/{id}` para um `subject` que não existe.
- **THEN** o sistema DEVE retornar um erro de "Não Encontrado" com um status HTTP 404.

### Requirement: Atualizar um Subject
O sistema DEVE permitir que um usuário autenticado atualize um `subject` que ele possui.

#### Scenario: Atualização bem-sucedida de um subject
- **WHEN** um usuário autenticado envia uma requisição PATCH para `/subjects/{id}` com dados válidos para um `subject` que ele possui.
- **THEN** o sistema DEVE atualizar o registro do `subject` no banco de dados.
- **AND** o sistema DEVE retornar os detalhes do `subject` atualizado com um status HTTP 200.

#### Scenario: Tentativa de atualizar um subject de outro usuário
- **WHEN** um usuário autenticado envia uma requisição PATCH para `/subjects/{id}` para um `subject` que ele não possui.
- **THEN** o sistema DEVE retornar um erro de "Não Autorizado" com um status HTTP 403.

### Requirement: Excluir um Subject
O sistema DEVE permitir que um usuário autenticado exclua um `subject` que ele possui.

#### Scenario: Exclusão bem-sucedida de um subject
- **WHEN** um usuário autenticado envia uma requisição DELETE para `/subjects/{id}` para um `subject` que ele possui.
- **THEN** o sistema DEVE excluir o registro do `subject` do banco de dados.
- **AND** o sistema DEVE retornar uma resposta de sucesso com um status HTTP 204.

#### Scenario: Tentativa de excluir um subject de outro usuário
- **WHEN** um usuário autenticado envia uma requisição DELETE para `/subjects/{id}` para um `subject` que ele não possui.
- **THEN** o sistema DEVE retornar um erro de "Não Autorizado" com um status HTTP 403.
