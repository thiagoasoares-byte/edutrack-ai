# Proposta: Endpoints CRUD para Tabela Subjects

## Why

A tabela `subjects` já existe no banco de dados, mas não possui endpoints REST para criar, ler, atualizar e deletar disciplinas. Sem essas APIs, o frontend não consegue gerenciar as disciplinas do usuário. Os endpoints devem respeitar a segurança de dados, garantindo que cada usuário acesse apenas suas próprias disciplinas.

## What Changes

Será criado um conjunto completo de endpoints CRUD (Create, Read, Update, Delete) com as seguintes operações:

- **POST /subjects** - Criar uma nova disciplina para o usuário autenticado
- **GET /subjects** - Listar todas as disciplinas do usuário autenticado
- **GET /subjects/{id}** - Obter os detalhes de uma disciplina específica
- **PATCH /subjects/{id}** - Atualizar uma disciplina existente
- **DELETE /subjects/{id}** - Deletar uma disciplina

Todos os endpoints incluirão validações de segurança:
- Apenas usuários autenticados podem acessar
- Cada usuário vê e modifica apenas suas próprias disciplinas
- Validação de entrada para campos obrigatórios e tipos
- Tratamento de erros consistente

## Impact

**Positivo:**
- Frontend terá APIs completas para gerenciar disciplinas
- Dados do usuário estarão protegidos (cada um acessa só seus dados)
- Reduzirá bugs relacionados a acesso indevido
- Preparará a aplicação para produção

**Escopo:**
- Apenas endpoints REST (implementação em XanoScript/Xano)
- Não inclui testes automatizados (a menos que solicitado)
- Não inclui alterações ao banco de dados (tabela já existe)
