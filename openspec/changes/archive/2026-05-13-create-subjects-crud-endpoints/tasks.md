## 1. Configuração do Endpoint POST /subjects

- [x] 1.1 Criar o endpoint `POST /subjects` no grupo de API `edutrack`.
- [x] 1.2 Configurar o endpoint para exigir autenticação.
- [x] 1.3 Adicionar lógica para inserir um novo registro na tabela `subjects`, definindo o `user_id` com o ID do usuário autenticado.
- [x] 1.4 Retornar o registro criado com o status 201.
- [x] 1.5 Testar o endpoint com um usuário autenticado e verificar a criação.
- [x] 1.6 Testar o endpoint sem autenticação e verificar o erro 401.

## 2. Configuração do Endpoint GET /subjects (Listar)

- [x] 2.1 Criar o endpoint `GET /subjects` no grupo de API `edutrack`.
- [x] 2.2 Configurar o endpoint para exigir autenticação.
- [x] 2.3 Adicionar lógica para consultar a tabela `subjects`, filtrando pelo `user_id` do usuário autenticado.
- [x] 2.4 Retornar a lista de registros com o status 200.
- [x] 2.5 Testar o endpoint para garantir que ele retorne apenas os `subjects` do usuário.

## 3. Configuração do Endpoint GET /subjects/{id} (Obter)

- [x] 3.1 Criar o endpoint `GET /subjects/{subjects_id}` no grupo de API `edutrack`.
- [x] 3.2 Configurar o endpoint para exigir autenticação.
- [x] 3.3 Adicionar um pré-requisito para buscar o `subject` pelo `subjects_id`.
- [x] 3.4 Adicionar lógica para verificar se o `user_id` do `subject` corresponde ao `auth:id`. Se não, retornar erro 403.
- [x] 3.5 Retornar o registro do `subject` com o status 200.
- [x] 3.6 Testar o acesso a um `subject` permitido.
- [x] 3.7 Testar o acesso a um `subject` de outro usuário e verificar o erro 403.
- [x] 3.8 Testar o acesso a um `subject` inexistente e verificar o erro 404.

## 4. Configuração do Endpoint PATCH /subjects/{id}

- [x] 4.1 Criar o endpoint `PATCH /subjects/{subjects_id}` no grupo de API `edutrack`.
- [x] 4.2 Configurar o endpoint para exigir autenticação.
- [x] 4.3 Reutilizar a lógica de verificação de propriedade do endpoint GET (item 3.4).
- [x] 4.4 Adicionar lógica para atualizar o registro na tabela `subjects`.
- [x] 4.5 Retornar o registro atualizado com o status 200.
- [x] 4.6 Testar a atualização de um `subject` permitido.
- [x] 4.7 Testar a tentativa de atualização de um `subject` de outro usuário e verificar o erro 403.

## 5. Configuração do Endpoint DELETE /subjects/{id}

- [x] 5.1 Criar o endpoint `DELETE /subjects/{subjects_id}` no grupo de API `edutrack`.
- [x] 5.2 Configurar o endpoint para exigir autenticação.
- [x] 5.3 Reutilizar a lógica de verificação de propriedade do endpoint GET (item 3.4).
- [x] 5.4 Adicionar lógica para excluir o registro da tabela `subjects`.
- [x] 5.5 Retornar uma resposta de sucesso com o status 204.
- [x] 5.6 Testar a exclusão de um `subject` permitido.
- [x] 5.7 Testar a tentativa de exclusão de um `subject` de outro usuário e verificar o erro 403.
