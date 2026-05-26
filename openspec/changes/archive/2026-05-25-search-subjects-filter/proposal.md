# Proposta: Endpoint de Busca para Subjects por Nome OU Tarefas Atrasadas

## Why

Os usuários precisam buscar disciplinas rapidamente por nome ou encontrar disciplinas com tarefas atrasadas. Um endpoint de busca que suporte ambos os filtros (com operador OU) simplifica a experiência do usuário e melhora produtividade.

## What Changes

- Adicionar um novo endpoint `GET /subjects/search` que aceita parâmetros de query:
  - `name` (string, opcional) — busca parcial (case-insensitive) no campo `name` da tabela `subjects`
  - `overdue` (boolean, opcional) — quando `true` inclui disciplinas que possuem tarefas atrasadas (due_date < now AND not completed)
  - `page`, `per_page` — paginação

- Lógica combinada: selecionar disciplinas que satisfaçam (name ILIKE %name%) OR (possuem tarefas atrasadas), sempre filtrando por `user_id` do usuário autenticado.

- Integração de lógica Python proposta para calcular eficientemente os `subject_id` que possuem tarefas atrasadas do usuário autenticado. Alternativa: implementar a lógica em XanoScript/SQL (preferível se desejarmos manter tudo no Xano).

## Impact

- Frontend poderá mostrar resultados combinados (nome OU overdue) em uma única chamada.
- Melhora na UX ao localizar disciplinas relevantes.
- Requer cuidado com performance: cálculo de tarefas atrasadas deve ser eficiente e respeitar `user_id`.

## Escopo

- Criar apenas o endpoint de busca (API). Não alterar a tabela `subjects`.
- Implementar helper em Python em `script/calculate_overdue_subjects.py` como opção; documentar como integrá-lo à pipeline do backend.
- Priorizar implementação em XanoScript se preferir manter tudo no Xano (documentar ambas as abordagens).