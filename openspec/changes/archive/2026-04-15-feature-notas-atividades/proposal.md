# Proposta: Feature de Lançamento de Notas

## Why (Por quê)

Atualmente, não há um mecanismo para que os professores registrem as notas dos alunos nas atividades acadêmicas. Esta funcionalidade é essencial para o acompanhamento do desempenho dos alunos e para a gestão do progresso do curso.

## What Changes (O que vai mudar)

Para habilitar o lançamento de notas, as seguintes mudanças serão implementadas:

1.  **Nova Tabela de Banco de Dados**:
    *   Criação da tabela `activity_grades` para armazenar a nota de um aluno em uma atividade específica, junto com a referência de quem a atribuiu.

2.  **Novo Endpoint de API**:
    *   Criação do endpoint `POST /activity_grades` que permitirá que um professor (usuário autenticado) insira uma nota para um aluno em uma atividade.

## Impact (Impacto)

*   **Adição**: Professores terão a capacidade de registrar notas para os alunos. O sistema agora armazenará essas informações de forma estruturada.
*   **Não incluso**: Esta mudança **não** inclui funcionalidades para listar, atualizar, ou deletar notas. Também não inclui a interface de usuário no frontend para o lançamento ou visualização das notas. O foco é estritamente na criação da infraestrutura de backend para o registro das notas.
