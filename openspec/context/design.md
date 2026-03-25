# Design: Tabela de Disciplinas (Subjects)

## 1. Visão Geral da Arquitetura

A solução consiste em criar uma nova tabela no banco de dados do Xano para armazenar as informações das disciplinas. Esta tabela será projetada para se relacionar com a tabela de usuários existente (`user`), estabelecendo a propriedade de cada disciplina.

## 2. Design da Tabela: `subjects`

A tabela `subjects` será criada no Xano com a seguinte estrutura:

| Campo      | Tipo      | Descrição                                         |
|------------|-----------|---------------------------------------------------|
| `id`       | `integer` | Chave primária, auto-incremento.                  |
| `created_at`| `timestamp`| Data e hora de criação do registro.              |
| `name`     | `text`    | O nome da disciplina (ex: "Cálculo I").           |
| `user_id`  | `integer` | Chave estrangeira para a tabela `user` (obrigatório). |

### Relacionamentos:
- **`subjects.user_id` -> `user.id`**: Um relacionamento de "um para muitos" será estabelecido, onde um usuário pode ter muitas disciplinas, mas cada disciplina pertence a apenas um usuário.