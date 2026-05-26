# Tarefas: Plano de Implementação por Papel

## Autenticação e Acesso
- [ ] Definir e criar endpoints de usuário no Xano com autenticação JWT.
- [ ] Implementar `POST /users` ou endpoint equivalente para cadastro.
- [ ] Implementar `POST /auth/login` ou endpoint equivalente para login.
- [ ] Implementar `GET /users/me` para recuperar perfil do usuário autenticado.
- [ ] Implementar `PATCH /users/me` para atualizar perfil do usuário.
- [ ] Planejar fluxo de reset de senha por e-mail.
- [ ] Planejar expiração de token e logout automático.
- [ ] Definir estratégia de persistência de sessão no frontend Streamlit.

## Gestão de Disciplinas
- [ ] Implementar `POST /subjects` para criar nova disciplina.
- [ ] Implementar `GET /subjects` para listar disciplinas do usuário.
- [ ] Implementar `GET /subjects/{id}` para obter disciplina por id.
- [ ] Implementar `PATCH /subjects/{id}` para atualizar disciplina.
- [ ] Implementar `DELETE /subjects/{id}` para excluir disciplina.
- [ ] Adicionar validação de propriedade para impedir acesso/edição por outros usuários.
- [ ] Adicionar validação de duplicidade por `name` + `teacher`.
- [ ] Criar busca por nome de disciplina.
- [ ] Criar filtro de disciplinas com tarefas em atraso.

## Gestão de Tarefas
- [ ] Implementar `POST /academic_tasks` para criar tarefa vinculada a disciplina.
- [ ] Implementar `GET /academic_tasks` para listar tarefas do usuário.
- [ ] Implementar `GET /academic_tasks/{id}` para detalhar tarefa.
- [ ] Implementar `PATCH /academic_tasks/{id}` para atualizar tarefa.
- [ ] Implementar `DELETE /academic_tasks/{id}` para excluir tarefa.
- [ ] Adicionar endpoint/fluxo para marcar tarefa como concluída.
- [ ] Adicionar filtros por status (`Pendente`, `Em andamento`, `Concluída`).
- [ ] Adicionar identificação e priorização de tarefas vencidas.
- [ ] Planejar agrupamento por disciplina e por prazo.

## Dashboard e Relatórios
- [ ] Definir métricas de dashboard pós-login.
- [ ] Implementar cálculo de total de disciplinas ativas.
- [ ] Implementar cálculo de total de tarefas pendentes e em atraso.
- [ ] Listar próximas tarefas por prazo.
- [ ] Calcular progresso geral (% concluído).
- [ ] Planejar relatório de histórico por período.
- [ ] Planejar relatório de progresso por disciplina.
- [ ] Planejar exportação de dados para CSV e PDF.

## Evolução da organização
- [ ] Planejar campo `semester` / `period` em `subjects`.
- [ ] Planejar campo `priority` em `academic_tasks` com valores `Baixa`, `Média`, `Alta`.
- [ ] Planejar cálculo de progresso por disciplina com base em tarefas concluídas.
- [ ] Planejar campo `archived` em `subjects` para arquivar em vez de excluir.

## UX / Design
- [ ] Criar identidade visual consistente para o frontend Streamlit.
- [ ] Melhorar layout de login e cadastro.
- [ ] Criar tela de boas-vindas para usuário sem dados.
- [ ] Adicionar confirmação antes de excluir disciplinas.
- [ ] Adicionar confirmação antes de excluir tarefas.
