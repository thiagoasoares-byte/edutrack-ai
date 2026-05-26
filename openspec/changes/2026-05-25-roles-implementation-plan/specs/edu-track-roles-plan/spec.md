# EduTrack Roles Implementation Specification

## Purpose

Documentar os requisitos funcionais para implementar autenticação, gestão de disciplinas, gestão de tarefas, dashboard, relatórios e evolução da organização no EduTrack AI.

## ADDED Requirements

### Requirement: Autenticação e gerenciamento de perfil
O sistema SHALL usar o `user` table com autenticação Xano e permitir cadastro, login, recuperação de perfil e atualização de perfil do usuário autenticado.

#### Scenario: Cadastro de usuário
- **WHEN** um visitante envia dados válidos para `POST /users`
- **THEN** sistema cria novo usuário e retorna 201 com token de acesso ou confirmação de cadastro

#### Scenario: Login do usuário
- **WHEN** um usuário envia credenciais válidas para `POST /auth/login`
- **THEN** sistema retorna token JWT válido e dados básicos do perfil

#### Scenario: Ler perfil autenticado
- **WHEN** usuário logado faz `GET /users/me`
- **THEN** sistema retorna dados do usuário atual

#### Scenario: Atualizar perfil autenticado
- **WHEN** usuário logado faz `PATCH /users/me` com dados válidos
- **THEN** sistema atualiza o perfil e retorna 200 com os dados atualizados

#### Scenario: Logout e expiração de token
- **WHEN** token expira ou usuário faz logout
- **THEN** sistema invalida a sessão e bloqueia acesso para endpoints protegidos

---

### Requirement: Subjects com CRUD e filtros
O sistema SHALL implementar endpoints CRUD para `subjects` garantindo propriedade por `user_id`, busca por nome e filtro de disciplinas com tarefas atrasadas.

#### Scenario: Criar disciplina
- **WHEN** usuário autenticado faz `POST /subjects` com `name` e `teacher`
- **THEN** sistema cria disciplina associada ao `user_id` do usuário

#### Scenario: Acessar apenas disciplinas do usuário
- **WHEN** usuário autenticado faz `GET /subjects` ou `GET /subjects/{id}`
- **THEN** sistema retorna apenas disciplinas cujo `user_id` corresponde ao usuário atual

#### Scenario: Atualizar e deletar com propriedade
- **WHEN** usuário tenta alterar ou excluir disciplina de outro usuário
- **THEN** sistema retorna 403 ou 404 e não permite a operação

#### Scenario: Buscar por nome
- **WHEN** usuário consulta `GET /subjects?name=text`
- **THEN** sistema retorna disciplinas do usuário com `name` parcialmente casando, case-insensitive

#### Scenario: Filtrar disciplinas overdue
- **WHEN** usuário consulta `GET /subjects?overdue=true`
- **THEN** sistema retorna disciplinas que possuam tarefas vencidas do usuário autenticado

#### Scenario: Prevenir duplicidade
- **WHEN** usuário tenta criar disciplina com mesmo `name` e `teacher`
- **THEN** sistema retorna erro de validação e não cria registro duplicado

---

### Requirement: Academic tasks com CRUD, status e overdue
O sistema SHALL implementar endpoints CRUD para `academic_tasks` com relacionamento indireto a `user` via `subject_id`, status de conclusão, filtros e priorização de tarefas vencidas.

#### Scenario: Criar tarefa vinculada a disciplina
- **WHEN** usuário autenticado faz `POST /academic_tasks` com `subject_id`, `title`, `due_date`
- **THEN** sistema cria tarefa somente se a disciplina existir e pertencer ao usuário

#### Scenario: Listar tarefas do usuário
- **WHEN** usuário faz `GET /academic_tasks`
- **THEN** sistema retorna apenas tarefas associadas a disciplinas do usuário autenticado

#### Scenario: Detalhar tarefa por id
- **WHEN** usuário faz `GET /academic_tasks/{id}`
- **THEN** sistema retorna tarefa somente se pertencer ao usuário

#### Scenario: Atualizar tarefa
- **WHEN** usuário faz `PATCH /academic_tasks/{id}` com dados válidos
- **THEN** sistema atualiza o registro após validar propriedade indireta

#### Scenario: Excluir tarefa
- **WHEN** usuário faz `DELETE /academic_tasks/{id}`
- **THEN** sistema exclui tarefa somente se pertencer ao usuário

#### Scenario: Filtrar por status e overdue
- **WHEN** usuário passa `status` ou `overdue` em `GET /academic_tasks`
- **THEN** sistema retorna tarefas correspondentes com base em `status` ou em `due_date < now()` e `status != "Concluída"`

#### Scenario: Agrupar por disciplina e prazo
- **WHEN** usuário solicita agrupamento nos parâmetros da API
- **THEN** sistema retorna tarefas agrupadas por `subject_id` ou por intervalo de prazo

---

### Requirement: Dashboard e relatórios
O sistema SHALL fornecer métricas e relatórios para o painel do usuário, incluindo totais de disciplinas, tarefas pendentes, tarefas em atraso, próximas tarefas e progresso.

#### Scenario: Painel pós-login
- **WHEN** usuário acessa o dashboard
- **THEN** sistema retorna métricas de disciplinas ativas, tarefas pendentes, tarefas atrasadas, próximas tarefas e progresso geral

#### Scenario: Relatório por período
- **WHEN** usuário filtra por intervalo de datas
- **THEN** sistema retorna histórico de tarefas e disciplinas dentro do período

#### Scenario: Progresso por disciplina
- **WHEN** usuário consulta progresso por disciplina
- **THEN** sistema retorna percentual de tarefas concluídas por disciplina

#### Scenario: Exportar dados
- **WHEN** usuário solicita exportação CSV ou PDF
- **THEN** sistema fornece dados ou payload adequado para geração de exportação

---

### Requirement: Evolução da organização
O sistema SHALL suportar campos opcionais para semestre/período em `subjects`, prioridade em `academic_tasks` e arquivamento de disciplinas.

#### Scenario: Adicionar semestre/período
- **WHEN** usuário insere `semester` ou `period` ao criar/atualizar disciplina
- **THEN** sistema salva essa informação para uso em filtros e relatórios

#### Scenario: Adicionar prioridade à tarefa
- **WHEN** usuário define `priority` em tarefa
- **THEN** sistema aceita valores `Baixa`, `Média`, `Alta` e permite ordenar por prioridade

#### Scenario: Arquivar disciplina
- **WHEN** usuário marca disciplina como arquivada
- **THEN** sistema mantém registro e o exclui das listas ativas sem apagá-lo definitivamente
