# Tasks: Endpoint de Busca Subjects (name OR overdue)

## Tarefas

- [ ] Ler guidelines `docs/api_query_guideline.md` e confirmar requisitos XanoScript
- [ ] Escrever spec OpenSpec final (`specs/subjects-search/spec.md`)
- [ ] Implementar endpoint `GET /subjects/search` em `apis/subjects/search.xs`
- [ ] Implementar helper Python opcional em `script/calculate_overdue_subjects.py` (documentar uso)
- [ ] Integrar helper ao endpoint (ou reimplementar lógica em XanoScript/SQL)
- [ ] Testar com curl/Postman e validar cenários (name, overdue, ambos)
- [ ] Documentar no `design.md` e marcar mudança pronta para arquivamento

## Notas

- A query deve sempre filtrar por `user_id` do usuário autenticado.
- Quando `overdue=true`, determinar `subject_id`s que têm tarefas atrasadas: `due_date < now()` e `completed = false`.
- O comportamento lógico é OR: resultados que satisfazem o filtro de nome OU possuem tarefas atrasadas.
- Evitar N+1: buscar IDs de subjects atrasados com uma única query/consulta agregada.
