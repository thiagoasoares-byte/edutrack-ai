# Design Técnico: Lançamento de Notas

Este documento detalha a implementação técnica para a funcionalidade de lançamento de notas.

## 1. Estrutura da Tabela `activity_grades`

Uma nova tabela será criada no Xano para armazenar as notas.

- **Nome da Tabela**: `activity_grades`
- **Campos**:
    - `id` (Integer, Primary Key, Auto-incremento)
    - `created_at` (Timestamp, Automático na criação)
    - `updated_at` (Timestamp, Automático na atualização)
    - `academic_task_id` (Integer, Relação com a tabela `academic_tasks`)
    - `student_id` (Integer, Relação com a tabela `users`)
    - `teacher_id` (Integer, Relação com a tabela `users`, armazena quem lançou a nota)
    - `grade` (Number, para armazenar a nota, ex: 8.5)
    - `comments` (Text, campo opcional para observações do professor)

## 2. API Endpoint `POST /activity_grades`

Será criado um endpoint para permitir o registro de uma nova nota.

- **Método**: `POST`
- **Endpoint**: `/activity_grades`
- **Autenticação**: Obrigatória. O usuário autenticado será considerado o `teacher_id`.

### Corpo da Requisição (Request Body)

O corpo da requisição deverá conter os seguintes campos:

```json
{
  "academic_task_id": 1,
  "student_id": 10,
  "grade": 8.5,
  "comments": "Ótimo trabalho na primeira parte da atividade."
}
```

### Lógica do Endpoint

1.  **Autenticação**: O endpoint deve garantir que o usuário está autenticado. O ID do usuário logado será usado como `teacher_id`.
2.  **Validação de Entrada**: Verificar se todos os campos obrigatórios (`academic_task_id`, `student_id`, `grade`) estão presentes.
3.  **Criação do Registro**: Inserir um novo registro na tabela `activity_grades` com os dados fornecidos na requisição e o `teacher_id` do usuário autenticado.
4.  **Resposta**:
    - Em caso de sucesso (código `201 Created`), retornar o registro da nota criada.
    - Em caso de erro de validação ou permissão (código `400 Bad Request` ou `403 Forbidden`), retornar uma mensagem de erro apropriada.
