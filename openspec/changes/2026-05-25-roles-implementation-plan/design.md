# Design: Plano de Implementação por Papel

## Contexto

O projeto já possui tabelas de dados centrais:
- `user` com `auth = true`
- `subjects` com `user_id` relacional
- `academic_tasks` com `subject_id`

A implementação deve garantir:
- autenticação e autorização centralizada no Xano;
- isolamento de dados por `user_id` e por propriedade de disciplina;
- consistência entre as operações CRUD e o fluxo de usuário.

## Arquitetura proposta

1. Autenticação e Acesso
  - Use o mecanismo de auth do Xano para o `user` table.
  - Endpoints de usuário devem operar com token JWT emitido pelo Xano.
  - Perfil do usuário recupera dados do `user` logado e permite atualização segura.

2. Subjects
  - `POST /subjects`: cria disciplina vinculada a `user_id` do usuário autenticado.
  - `GET /subjects`: lista apenas disciplinas do usuário autenticado.
  - `GET /subjects/{id}`: retorna disciplina se `user_id` corresponder.
  - `PATCH /subjects/{id}` e `DELETE /subjects/{id}`: valida propriedade antes de alterar.
  - Validação de duplicidade: impedir dois registros do mesmo `name` e `teacher` para o mesmo usuário.
  - Busca/filtro: `name` parcial e `overdue` baseado em tarefas atrasadas.

3. Academic Tasks
  - `POST /academic_tasks`: cria tarefa vinculada a disciplina existente.
  - `GET /academic_tasks`: lista tarefas do usuário autorizado, usando join indireto via `subject_id`.
  - `GET /academic_tasks/{id}`: detalhe somente se a tarefa pertence a disciplina do usuário.
  - Atualização e exclusão seguem validação de propriedade indireta.
  - Marcação de conclusão atualiza `status` e mantém `due_date`.
  - Filtros por status e overdue.
  - Agrupamento pode ser feito no frontend ou via API com parâmetro `group_by`.

4. Dashboard e Relatórios
  - Endpoints ou queries Xano devem calcular:
    - total de disciplinas ativas
    - total de tarefas pendentes e atrasadas
    - próximas tarefas ordenadas por prazo
    - progresso geral (% concluído)
  - Relatórios de histórico por período usam filtros de data em `due_date` e `created_at`.
  - Progresso por disciplina é calculado por `tarefas concluídas / total de tarefas`.
  - Exportação: gerar dados estruturados para CSV e PDF no frontend; API retorna payload amigável para export.

5. Evolução da organização
  - Adicionar campos de metadata em `subjects` e `academic_tasks` quando for implementar:
    - `semester` ou `period` na tabela `subjects`
    - `priority` na tabela `academic_tasks`
    - `archived` em `subjects` para disciplinas concluídas
  - Esses campos permitem filtros, relatórios e organização avançada.

6. UX / Design
  - Layout de login/cadastro deve ser claro e acessível.
  - Tela de boas-vindas para usuário novo deve explicar como começar.
  - Alertas de confirmação ao excluir disciplinas ou tarefas.
  - Identidade visual consistente entre pages do Streamlit.
