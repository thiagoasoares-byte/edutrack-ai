# Subjects Search Specification

## Purpose

Adicionar um endpoint de busca que permita filtrar disciplinas por `name` OU por `tarefas atrasadas` (overdue), garantindo que cada usuário veja apenas suas disciplinas.

## ADDED Requirements

### Requirement: Criar endpoint GET /subjects/search

Sistema SHALL permitir buscas por `name` (parcial, case-insensitive) e/ou por `overdue` (boolean) e retornar disciplinas do usuário autenticado que satisfaçam a condição OU.

#### Scenario: Buscar por nome
- **WHEN** usuário autenticado faz GET /subjects/search?name=math
- **THEN** sistema retorna 200 OK com disciplinas do usuário cujo `name` casem parcialmente

#### Scenario: Buscar por overdue
- **WHEN** usuário autenticado faz GET /subjects/search?overdue=true
- **THEN** sistema retorna 200 OK com disciplinas que possuem pelo menos uma tarefa atrasada (`due_date < now()` e `completed = false`) do usuário

#### Scenario: Buscar por name OU overdue
- **WHEN** usuário autenticado faz GET /subjects/search?name=calc&overdue=true
- **THEN** sistema retorna 200 OK com disciplinas que satisfazem (name ILIKE %calc%) OR (possuem tarefas atrasadas) filtradas por `user_id`

#### Scenario: Sem parâmetros
- **WHEN** chamada sem `name` nem `overdue`
- **THEN** sistema retorna 400 Bad Request ou trata como GET /subjects (definir comportamento) — RECOMENDADO: retornar 400 pedindo pelo menos um filtro

---

### Requirement: Segurança

- Sistema SHALL validar autenticação e filtrar por `user_id` em todas as consultas.
- Sistema SHALL evitar exposição de disciplinas de outros usuários.

---

### Requirement: Performance

- Sistema SHOULD usar consulta agregada para determinar `subject_id`s com tarefas atrasadas.
- Sistema SHOULD limitar `per_page` em 100.
