## Context

A proposta descreve a necessidade de criar endpoints CRUD para a tabela `subjects`. Atualmente, não há como interagir com essa tabela através da API. Esta mudança se concentrará na implementação desses endpoints no Xano, garantindo que a segurança em nível de registro seja aplicada para que os usuários só possam acessar os `subjects` que possuem.

## Goals / Non-Goals

**Goals:**
- Implementar os endpoints POST, GET, PATCH e DELETE para `subjects`.
- Garantir que todos os endpoints exijam autenticação.
- Implementar a lógica de autorização para restringir o acesso com base no `user_id` do registro.
- Os endpoints serão adicionados ao grupo de API `edutrack` existente.

**Non-Goals:**
- Criar a interface de usuário para gerenciar `subjects`.
- Implementar recursos avançados como paginação ou filtragem complexa na listagem de GET (além da filtragem por usuário).
- Modificar o esquema da tabela `subjects` existente.

## Decisions

1.  **Autenticação**:
    - **Decisão**: Utilizar o sistema de autenticação de token existente do Xano.
    - **Justificativa**: É o padrão da plataforma, seguro e já está em uso em outras partes da aplicação. A tabela `user` já existe e está configurada para autenticação.

2.  **Autorização**:
    - **Decisão**: A autorização será implementada em cada endpoint da API.
        - Para **POST**, o `user_id` do usuário autenticado será adicionado automaticamente ao novo registro do `subject`.
        - Para **GET (lista)**, a consulta ao banco de dados será filtrada pelo `user_id` do usuário autenticado.
        - Para **GET (single)**, **PATCH** e **DELETE**, um pré-requisito (Preprocessor) verificará se o `user_id` do registro do `subject` corresponde ao `user_id` do usuário autenticado. Se não corresponder, a API retornará um erro de "Não Autorizado".
    - **Justificativa**: Essa abordagem garante que a propriedade dos dados seja aplicada de forma consistente em todas as operações, prevenindo o acesso não autorizado aos dados de outros usuários.

3.  **Estrutura da API**:
    - **Decisão**: Os endpoints seguirão as convenções RESTful padrão.
        - `POST /subjects`
        - `GET /subjects`
        - `GET /subjects/{subjects_id}`
        - `PATCH /subjects/{subjects_id}`
        - `DELETE /subjects/{subjects_id}`
    - **Justificativa**: A adesão aos padrões REST facilita a compreensão e o consumo da API. O uso de `{subjects_id}` como parâmetro de rota é consistente com as melhores práticas.

## Risks / Trade-offs

- **Risco**: Se a lógica de autorização não for implementada corretamente em todos os endpoints, pode haver vazamento de dados.
    - **Mitigação**: Testes rigorosos serão criados para cada endpoint para verificar os cenários de sucesso (usuário acessando seus próprios dados) e de falha (usuário tentando acessar dados de outros).
