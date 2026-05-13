## Why

Atualmente, não existem endpoints de API para gerenciar a tabela `subjects`. Esta mudança introduzirá endpoints CRUD (Criar, Ler, Atualizar, Excluir) para permitir que os usuários gerenciem seus próprios `subjects` de forma segura.

## What Changes

- **POST /subjects**: Cria um novo `subject`.
- **GET /subjects**: Retorna uma lista de `subjects` do usuário autenticado.
- **GET /subjects/{id}**: Retorna um único `subject` pelo ID.
- **PATCH /subjects/{id}**: Atualiza um `subject` existente.
- **DELETE /subjects/{id}**: Exclui um `subject`.
- Adiciona autenticação e autorização para garantir que os usuários só possam acessar seus próprios dados.

## Capabilities

### New Capabilities
- `subjects-api`: Fornece endpoints CRUD para gerenciar `subjects`, com autorização baseada no proprietário.

### Modified Capabilities
- *Nenhuma*

## Impact

- **API**: Novos endpoints serão adicionados ao grupo de API `edutrack`.
- **Banco de Dados**: As operações CRUD interagirão com a tabela `subjects`.
- **Segurança**: A lógica de autorização será implementada para restringir o acesso aos dados.
