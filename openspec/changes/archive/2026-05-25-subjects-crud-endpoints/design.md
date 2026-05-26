# Design: Endpoints CRUD para Subjects

## Visão Geral

Os endpoints CRUD serão implementados em XanoScript (Xano) e integrados ao frontend Streamlit.

## Estrutura de Dados

### Tabela: subjects

Campos esperados (conforme spec da tabela):
- `id` - Identificador único (int/uuid)
- `user_id` - Referência ao usuário proprietário
- `name` - Nome da disciplina (texto)
- `description` - Descrição (opcional)
- Outros campos conforme necessário

## Endpoints

### 1. POST /subjects - Criar Disciplina

**Entrada:**
```json
{
  "name": "Matemática Avançada",
  "description": "Cálculo diferencial e integral"
}
```

**Processamento:**
- Validar que `name` é obrigatório e não vazio
- Atribuir `user_id` do usuário autenticado
- Inserir na tabela `subjects`
- Retornar o objeto criado

**Saída (201 Created):**
```json
{
  "id": 1,
  "user_id": "user_123",
  "name": "Matemática Avançada",
  "description": "Cálculo diferencial e integral",
  "created_at": "2026-05-25T10:30:00Z"
}
```

---

### 2. GET /subjects - Listar Disciplinas do Usuário

**Parâmetros:**
- Filtro por `user_id` automático (do usuário autenticado)
- Opcionais: paginação, ordenação

**Processamento:**
- Filtrar por `user_id` do usuário autenticado
- Retornar lista de todas as disciplinas

**Saída (200 OK):**
```json
[
  {
    "id": 1,
    "user_id": "user_123",
    "name": "Matemática Avançada",
    "description": "Cálculo diferencial e integral"
  },
  {
    "id": 2,
    "user_id": "user_123",
    "name": "Física",
    "description": "Mecânica Clássica"
  }
]
```

---

### 3. GET /subjects/{id} - Obter Disciplina Específica

**Parâmetros:**
- `id` (path parameter) - Identificador da disciplina

**Processamento:**
- Buscar disciplina com esse ID
- Validar que `user_id` corresponde ao usuário autenticado
- Retornar erro 403/404 se não pertencer ao usuário

**Saída (200 OK):**
```json
{
  "id": 1,
  "user_id": "user_123",
  "name": "Matemática Avançada",
  "description": "Cálculo diferencial e integral"
}
```

---

### 4. PATCH /subjects/{id} - Atualizar Disciplina

**Parâmetros:**
- `id` (path parameter)

**Entrada:**
```json
{
  "name": "Matemática Avançada - Revisão",
  "description": "Cálculo diferencial, integral e álgebra linear"
}
```

**Processamento:**
- Buscar disciplina com esse ID
- Validar que `user_id` corresponde ao usuário autenticado
- Atualizar apenas os campos fornecidos
- Validar campos não vazios
- Retornar erro 403/404 se não pertencer ao usuário

**Saída (200 OK):**
```json
{
  "id": 1,
  "user_id": "user_123",
  "name": "Matemática Avançada - Revisão",
  "description": "Cálculo diferencial, integral e álgebra linear"
}
```

---

### 5. DELETE /subjects/{id} - Deletar Disciplina

**Parâmetros:**
- `id` (path parameter)

**Processamento:**
- Buscar disciplina com esse ID
- Validar que `user_id` corresponde ao usuário autenticado
- Deletar o registro
- Retornar erro 403/404 se não pertencer ao usuário

**Saída (204 No Content):**
- Sem corpo (ou `{}`)

---

## Segurança

1. **Autenticação:** Todos os endpoints requerem token de autenticação
2. **Autorização:** Filtro por `user_id` obrigatório em todas as queries
3. **Validação:** Campos obrigatórios, tipos corretos, tamanho máximo de strings
4. **Tratamento de Erros:**
   - `400 Bad Request` - Entrada inválida
   - `401 Unauthorized` - Sem token/token inválido
   - `403 Forbidden` - Sem permissão para acessar recurso
   - `404 Not Found` - Recurso não existe
   - `500 Internal Server Error` - Erro no servidor

## Próximos Passos

1. Verificar os guidelines de API do XanoScript em `/docs/api_query_guideline.md`
2. Usar o **Xano API Query Writer** para implementar cada endpoint
3. Testar cada endpoint individualmente
4. Validar permissões de usuário
