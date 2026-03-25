# Proposta: Criar Base de Dados para Disciplinas (Subjects)

## O Quê?

Esta mudança introduzirá a estrutura de banco de dados fundamental para o gerenciamento de disciplinas acadêmicas (`subjects`). A principal ação será a criação de uma nova tabela `subjects` no Xano.

## Por Quê?

Atualmente, o sistema não possui uma forma de armazenar ou gerenciar as disciplinas de um usuário. A criação desta tabela é o primeiro passo essencial para construir funcionalidades mais complexas, como:

- Listar as disciplinas de um usuário.
- Associar tarefas e notas a uma disciplina.
- Permitir que os usuários gerenciem suas informações acadêmicas.

Esta base é crucial para o propósito central do EduTrack AI, que é ser um assistente acadêmico.

## Não-Metas

- **Criação de APIs:** As APIs para interagir com esta tabela (criar, ler, atualizar, deletar) serão desenvolvidas em uma mudança futura.
- **Interface do Usuário:** Nenhuma alteração na interface do Streamlit será feita nesta etapa.
- **Tarefas ou Notas:** A criação de tabelas relacionadas como `tasks` ou `grades` não faz parte deste escopo.