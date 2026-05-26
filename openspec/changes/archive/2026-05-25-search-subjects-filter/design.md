# Design: Endpoint `GET /subjects/search`

## Entrada (query parameters)
- `name` (string, optional) — busca parcial, case-insensitive
- `overdue` (boolean, optional) — se `true`, incluir disciplinas com tarefas atrasadas
- `page` (int) — paginação
- `per_page` (int) — itens por página

## Saída
- 200 OK com lista paginada de disciplinas (formatado como no endpoint `GET /subjects`)

## Lógica proposta

1. Normalizar `name` (trim, lowercase) se fornecido.
2. Se `overdue=true`:
   - Opção A (recomendada): executar query para coletar `subject_id` que possuem tarefas atrasadas do usuário autenticado em uma única consulta agregada:
     - SQL/XanoScript: SELECT DISTINCT subject_id FROM tasks WHERE user_id = $auth.id AND completed = false AND due_date < now()
   - Opção B: chamar helper Python `script/calculate_overdue_subjects.py` que conecta ao DB e retorna ids (use quando lógica for complexa).
3. Montar filtro final para `subjects`:
   - Se `name` e `overdue`: WHERE (subjects.name ILIKE %name%) OR (subjects.id IN (overdue_ids)) AND subjects.user_id = $auth.id
   - Respeitar precedência: aplicar `user_id` em ambos os lados.
4. Executar `db.query "subjects"` com `where` composto e paginação.

## Integração Python (opcional)
- Local: `script/calculate_overdue_subjects.py`
- Função: `get_overdue_subject_ids(db_conn, user_id) -> List[int]`
- Vantagem: lógica reutilizável e testável; pode ser usada por outros jobs.
- Desvantagem: adiciona componente externo (deploy e autenticação entre serviços).

## Considerações de Segurança e Performance
- Sempre filtrar por `$auth.id`.
- Indexes: garantir index em `tasks(subject_id, user_id, due_date, completed)` para performance.
- Limitar `per_page` (ex: max 100)
- Evitar retornar dados de outros usuários

## Exemplos de uso
- `GET /subjects/search?name=math`
- `GET /subjects/search?overdue=true`
- `GET /subjects/search?name=calc&overdue=true&page=2&per_page=20`