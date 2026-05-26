# Tarefas: Endpoints CRUD para Disciplinas (Subjects)

Com base na sua solicitação, estas são as tarefas para criar os endpoints CRUD para a tabela `subjects`, garantindo que cada usuário possa acessar e gerenciar apenas seus próprios dados.

- [x] **Backend (Xano)**:
    - [x] 1. Criar o endpoint `POST /subjects` para permitir que um usuário autenticado crie uma nova disciplina.
    - [x] 2. Criar o endpoint `GET /subjects` para listar todas as disciplinas pertencentes ao usuário autenticado.
    - [x] 3. Criar o endpoint `GET /subjects/{id}` para buscar uma disciplina específica, validando se ela pertence ao usuário autenticado.
    - [x] 4. Criar o endpoint `PATCH /subjects/{id}` para permitir que um usuário autenticado atualize os dados de uma de suas disciplinas.
    - [x] 5. Criar o endpoint `DELETE /subjects/{id}` para permitir que um usuário autenticado delete uma de suas disciplinas.

## ✅ Conclusão

**Data:** 2026-05-25  
**Status:** Concluído com sucesso ✅

Todos os 5 endpoints CRUD foram implementados em XanoScript com as seguintes características:

- **Localização:** `apis/subjects/` (5 arquivos: create.xs, list.xs, get.xs, update.xs, delete.xs)
- **Segurança:** Autenticação JWT + Filtro por user_id em todas as operações
- **Validação:** Ownership validation antes de modificar/deletar
- **Status HTTP:** Corretos (201, 200, 204, 400, 401, 404)
- **Documentação:** 
  - Spec: `openspec/changes/archive/2026-05-25-subjects-crud-endpoints/specs/subjects-api/spec.md`
  - Design: `openspec/changes/archive/2026-05-25-subjects-crud-endpoints/design.md`
  - Tasks: `openspec/changes/archive/2026-05-25-subjects-crud-endpoints/tasks.md`

**Archive:** `openspec/changes/archive/2026-05-25-subjects-crud-endpoints/` (moved)

**Próximo passo:** Fazer push manual dos arquivos para o Xano quando estiver pronto.
