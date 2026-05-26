# Tasks: Endpoints CRUD para Subjects

## Tarefas

- [ ] Criar API POST /subjects (Create)
- [ ] Criar API GET /subjects (Read - Listar)
- [ ] Criar API GET /subjects/{id} (Read - Detalhe)
- [ ] Criar API PATCH /subjects/{id} (Update)
- [ ] Criar API DELETE /subjects/{id} (Delete)

## Notas de Implementação

- Todos os endpoints devem filtrar por `user_id` do usuário autenticado
- Validar que o ID fornecido pertence ao usuário antes de modificar/deletar
- Retornar erro 404 ou 403 se recurso não existir ou não pertencer ao usuário
- Usar status HTTP apropriados (201 para CREATE, 200 para sucesso, 204 para DELETE, etc.)
